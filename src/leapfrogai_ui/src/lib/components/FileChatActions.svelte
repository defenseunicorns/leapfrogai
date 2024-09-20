<script lang="ts">
  import { Button } from 'flowbite-svelte';
  import { v4 as uuidv4 } from 'uuid';
  import { fade } from 'svelte/transition';
  import { shortenFileName } from '$helpers/stringHelpers';
  import { saveMessage } from '$helpers/chatHelpers';
  import type { FileMetadata, LFFile } from '$lib/types/files';
  import { threadsStore, toastStore } from '$stores';
  import {
    AUDIO_FILE_SIZE_ERROR_TOAST,
    FILE_SUMMARIZATION_ERROR,
    FILE_TRANSCRIPTION_ERROR,
    FILE_TRANSLATION_ERROR
  } from '$constants/toastMessages';
  import { tick } from 'svelte';
  import { page } from '$app/stores';
  import type { Message } from 'ai';
  import { AUDIO_FILE_SIZE_ERROR_TEXT, STANDARD_FADE_DURATION } from '$constants';
  import type { AppendFunction } from '$lib/types/messages';
  import LFCarousel from '$components/LFCarousel.svelte';

  export let attachedFiles: LFFile[];
  export let attachedFileMetadata: FileMetadata[];
  export let threadId: string;
  export let originalMessages: Message[];
  export let setMessages: (messages: Message[]) => void;
  export let append: AppendFunction;

  type MethodType = 'translation' | 'transcription' | 'summarization';
  let processing: { fileId: string; method: MethodType } = {};

  $: audioFiles = attachedFileMetadata.filter((file) => file.type.startsWith('audio/'));
  $: nonAudioFiles = attachedFileMetadata.filter((file) => !file.type.startsWith('audio/'));

  const customBtnClass =
    'rounded text-xs px-2.5 py-0.5 text-gray-500 bg-gray-100 hover:bg-gray-400 dark:bg-gray-100 dark:text-gray-900 dark:hover:bg-gray-300 truncate';

  const reset = async () => {
    await threadsStore.setSendingBlocked(false);
    processing = {};
  };

  const handleGeneralError = async (toastData: ToastData) => {
    toastStore.addToast(toastData);
    if (processing.fileId) {
      const fileMetadataIndex = attachedFiles.findIndex((f) => f.id === processing.fileId);
      attachedFileMetadata[fileMetadataIndex] = {
        ...attachedFileMetadata[fileMetadataIndex],
        status: 'error',
        errorText: toastData.subtitle
      };
    }
    await reset();
  };

  const transcribeOrTranslate = async (fileMetadata: FileMetadata, method: MethodType) => {
    const toastError =
      method === 'translation' ? FILE_TRANSLATION_ERROR() : FILE_TRANSCRIPTION_ERROR();

    const adjective = method === 'translation' ? ' Translate' : 'Transcribe';

    const attachedFileMetadataCopy = [...attachedFileMetadata];
    const attachedFilesCopy = [...attachedFiles];
    // Remove the file and file metadata to hide the actions since the response will stream in this case
    attachedFiles = attachedFiles.filter((file) => file.id !== fileMetadata.id);
    attachedFileMetadata = attachedFileMetadata.filter((file) => file.id !== fileMetadata.id);

    if (!fileMetadata.id) {
      await handleGeneralError(toastError);
      return;
    }
    processing = { fileId: fileMetadata.id, method };

    const file = attachedFilesCopy.find((f) => f.id === fileMetadata.id);
    const metadataToSave = attachedFileMetadataCopy.find((f) => f.id === fileMetadata.id);
    if (!file || !metadataToSave) {
      await handleGeneralError(toastError);
      return;
    }

    await threadsStore.setSendingBlocked(true);
    let tempId: string;
    try {
      if (!threadId) {
        // create new thread
        await threadsStore.newThread(`${adjective} ${fileMetadata.name}`);
        await tick(); // allow store to update
        threadId = $page.params.thread_id;
      }

      // Save new user message
      const newMessage = await saveMessage({
        thread_id: threadId,
        content: `${adjective} ${file.name}`, // use full name instead of metadata name which might be truncated
        role: 'user',
        metadata: {
          filesMetadata: JSON.stringify([metadataToSave]),
          wasTranscriptionOrTranslation: 'true'
        }
      });
      await threadsStore.addMessageToStore(newMessage);
      threadsStore.updateMessagesState(originalMessages, setMessages, newMessage);

      tempId = uuidv4();
      await threadsStore.addTempEmptyMessage(threadId, tempId);

      // translate
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch(`/api/audio/${method}`, {
        method: 'POST',
        body: formData
      });
      const resJson = await res.json();
      if (!res.ok) {
        if (resJson.message === `ValidationError: ${AUDIO_FILE_SIZE_ERROR_TEXT}`) {
          await handleGeneralError(AUDIO_FILE_SIZE_ERROR_TOAST());
        } else {
          await handleGeneralError(toastError);
        }
        return;
      }

      // save translation response
      let responseMessage;
      try {
        responseMessage = await saveMessage({
          thread_id: threadId,
          content: resJson.text,
          role: 'assistant',
          metadata: {
            wasTranscriptionOrTranslation: 'true'
          }
        });
      } catch {
        await handleGeneralError(toastError);
        responseMessage = await saveMessage({
          thread_id: threadId,
          content: 'There was an error translating the file',
          role: 'assistant',
          metadata: {
            wasTranscriptionOrTranslation: 'true'
          }
        });
      }

      threadsStore.replaceTempMessageWithActual(threadId, tempId, responseMessage);
      threadsStore.updateMessagesState(originalMessages, setMessages, responseMessage);
    } catch {
      if (tempId) {
        threadsStore.removeMessageFromStore(threadId, tempId);
      }
      await handleGeneralError(toastError);
      return;
    }

    await reset();
  };

  const summarize = async (fileMetadata: FileMetadata) => {
    const attachedFileMetadataCopy = [...attachedFileMetadata];
    // Remove the file and file metadata to hide the actions since the response will stream in this case
    attachedFiles = attachedFiles.filter((file) => file.id !== fileMetadata.id);
    attachedFileMetadata = attachedFileMetadata.filter((file) => file.id !== fileMetadata.id);

    const toastError = FILE_SUMMARIZATION_ERROR();

    if (!fileMetadata.id) {
      await handleGeneralError(toastError);
      return;
    }
    processing = { fileId: fileMetadata.id, method: 'summarization' };

    await threadsStore.setSendingBlocked(true);
    try {
      if (!threadId) {
        // create new thread
        await threadsStore.newThread(`Summarize ${fileMetadata.name}`);
        await tick(); // allow store to update
        threadId = $page.params.thread_id;
      }

      const metadataToSave = attachedFileMetadataCopy.find((f) => f.id === fileMetadata.id);
      if (!metadataToSave) {
        await handleGeneralError(toastError);
        return;
      }
      // Save file info to context
      await saveMessage({
        thread_id: threadId,
        content: `The following is the text content of a file named ${fileMetadata.name}: ${fileMetadata.text}`,
        role: 'user',
        metadata: {
          hideMessage: 'true'
        },
        lengthOverride: true
      });

      // Save new user message
      const content = `Summarize ${fileMetadata.name}`;
      const newMessage = await saveMessage({
        thread_id: threadId,
        content,
        role: 'user',
        metadata: {
          filesMetadata: JSON.stringify([metadataToSave])
        }
      });

      await threadsStore.addMessageToStore(newMessage);

      // Append will handle state update, threadsStore.updateMessagesState not necessary
      await append({
        content,
        role: 'user',
        createdAt: new Date()
      });
    } catch {
      await handleGeneralError(toastError);
      return;
    }

    await reset();
  };
</script>

<LFCarousel
  data-testid="file-actions-carousel"
  hidden={nonAudioFiles.length + audioFiles.length === 0}
>
  <div
    id="uploaded-files-actions"
    class={nonAudioFiles.length + audioFiles.length > 0 ? 'flex gap-2  py-2' : 'hidden'}
  >
    {#each audioFiles as file}
      {#if file.status === 'complete'}
        <div in:fade={{ duration: STANDARD_FADE_DURATION }}>
          <Button
            color="dark"
            class={customBtnClass}
            on:click={() => transcribeOrTranslate(file, 'translation')}
            disabled={processing.fileId}
          >
            {`Translate ${shortenFileName(file.name)}`}</Button
          >
        </div>
        <div in:fade={{ duration: STANDARD_FADE_DURATION }}>
          <Button
            color="dark"
            class={customBtnClass}
            on:click={() => transcribeOrTranslate(file, 'transcription')}
            disabled={processing.fileId}
          >
            {`Transcribe ${shortenFileName(file.name)}`}</Button
          >
        </div>
      {/if}
    {/each}
    {#each nonAudioFiles as file}
      {#if file.status === 'complete'}
        <div
          in:fade={{ duration: STANDARD_FADE_DURATION }}
          out:fade={{ duration: STANDARD_FADE_DURATION }}
        >
          <Button
            color="dark"
            class={customBtnClass}
            on:click={() => summarize(file)}
            disabled={processing.fileId}
          >
            {`Summarize ${shortenFileName(file.name)}`}</Button
          >
        </div>
      {/if}
    {/each}
  </div>
</LFCarousel>
