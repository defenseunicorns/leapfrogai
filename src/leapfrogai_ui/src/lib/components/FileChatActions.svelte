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
    FILE_TRANSCRIPTION_ERROR,
    FILE_TRANSLATION_ERROR
  } from '$constants/toastMessages';
  import { tick } from 'svelte';
  import { page } from '$app/stores';
  import type { Message } from 'ai';
  import { AUDIO_FILE_SIZE_ERROR_TEXT } from '$constants';

  export let attachedFiles: LFFile[];
  export let attachedFileMetadata: FileMetadata[];
  export let threadId: string;
  export let originalMessages: Message[];
  export let setMessages: (messages: Message[]) => void;

  type MethodType = 'translation' | 'transcription';
  let processing: { fileId: string; method: MethodType } = {};

  $: audioFiles = attachedFileMetadata.filter((file) => file.type.startsWith('audio/'));

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
</script>

<div
  id="uploaded-files-actions"
  class={audioFiles.length > 0
    ? 'ml-6 flex max-w-full gap-2 overflow-x-auto bg-gray-700'
    : 'hidden'}
>
  {#each audioFiles as file}
    <div in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
      <Button
        color="dark"
        class={customBtnClass}
        on:click={() => transcribeOrTranslate(file, 'translation')}
        disabled={processing.fileId}
      >
        {`Translate ${shortenFileName(file.name)}`}</Button
      >
    </div>
  {/each}
  {#each audioFiles as file}
    <div in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
      <Button
        color="dark"
        class={customBtnClass}
        on:click={() => transcribeOrTranslate(file, 'transcription')}
        disabled={processing.fileId}
      >

          {`Transcribe ${shortenFileName(file.name)}`}</Button
      >
    </div>
  {/each}
</div>
