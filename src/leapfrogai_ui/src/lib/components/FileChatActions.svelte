<script lang="ts">
  import { Button, Spinner } from 'flowbite-svelte';
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
  import { AUDIO_FILE_SIZE_ERROR_TEXT } from '$constants';
  import type { AppendFunction } from '$lib/types/messages';

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

    if (!fileMetadata.id) {
      await handleGeneralError(toastError);
      return;
    }
    processing = { fileId: fileMetadata.id, method };

    await threadsStore.setSendingBlocked(true);
    try {
      if (!threadId) {
        // create new thread
        await threadsStore.newThread(`${adjective} ${fileMetadata.name}`);
        await tick(); // allow store to update
        threadId = $page.params.thread_id;
      }

      const metadataToSave = attachedFileMetadata.find((f) => f.id === fileMetadata.id);
      if (!metadataToSave) {
        await handleGeneralError(toastError);
        return;
      }
      // Save new user message
      const newMessage = await saveMessage({
        thread_id: threadId,
        content: `${adjective} ${fileMetadata.name}`,
        role: 'user',
        metadata: {
          filesMetadata: JSON.stringify([metadataToSave])
        }
      });
      await threadsStore.addMessageToStore(newMessage);
      threadsStore.updateMessagesState(originalMessages, setMessages, newMessage);

      // translate
      const file = attachedFiles.find((f) => f.id === fileMetadata.id);
      if (!file) {
        await handleGeneralError(toastError);
        return;
      }

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
      const responseMessage = await saveMessage({
        thread_id: threadId,
        content: resJson.text,
        role: 'assistant'
      });
      await threadsStore.addMessageToStore(responseMessage);
      threadsStore.updateMessagesState(originalMessages, setMessages, responseMessage);
      attachedFiles = attachedFiles.filter((file) => file.id !== fileMetadata.id);
      attachedFileMetadata = attachedFileMetadata.filter((file) => file.id !== fileMetadata.id);
    } catch {
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

<div
  id="uploaded-files-actions"
  class={nonAudioFiles.length + audioFiles.length > 0
    ? 'ml-6 flex max-w-full gap-2 overflow-x-auto bg-gray-700'
    : 'hidden'}
>
  {#each audioFiles as file}
    {#if file.status === 'complete'}
      <div in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
        <Button
          color="dark"
          class={customBtnClass}
          on:click={() => transcribeOrTranslate(file, 'translation')}
          disabled={processing.fileId}
        >
          {#if processing.fileId === file.id && processing.method === 'translation'}
            <Spinner class="me-2" size="2" color="white" data-testid="translation-spinner" /><span
              >{`Translating ${shortenFileName(file.name)}`}</span
            >
          {:else}
            {`Translate ${shortenFileName(file.name)}`}{/if}</Button
        >
      </div>
    {/if}
  {/each}
  {#each audioFiles as file}
    {#if file.status === 'complete'}
      <div in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
        <Button
          color="dark"
          class={customBtnClass}
          on:click={() => transcribeOrTranslate(file, 'transcription')}
          disabled={processing.fileId}
        >
          {#if processing.fileId === file.id && processing.method === 'transcription'}
            <Spinner class="me-2" size="2" color="white" data-testid="transcription-spinner" /><span
              >{`Transcribing ${shortenFileName(file.name)}`}</span
            >
          {:else}
            {`Transcribe ${shortenFileName(file.name)}`}{/if}</Button
        >
      </div>
    {/if}
  {/each}
  {#each nonAudioFiles as file}
    {#if file.status === 'complete'}
      <div in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
        <Button
          color="dark"
          class={customBtnClass}
          on:click={() => summarize(file)}
          disabled={processing.fileId}
        >
          {#if processing.fileId === file.id && processing.method === 'summarization'}
            <Spinner class="me-2" size="2" color="white" data-testid="summarization-spinner" /><span
              >{`Summarizing ${shortenFileName(file.name)}`}</span
            >
          {:else}
            {`Summarize ${shortenFileName(file.name)}`}{/if}</Button
        >
      </div>
    {/if}
  {/each}
</div>
