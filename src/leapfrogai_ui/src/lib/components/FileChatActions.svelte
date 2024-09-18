<script lang="ts">
  import { Button, Spinner } from 'flowbite-svelte';
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

  let fileId: string;

  $: audioFiles = attachedFileMetadata.filter((file) => file.type.startsWith('audio/'));

  const customBtnClass =
    'rounded text-xs px-2.5 py-0.5 text-gray-500 bg-gray-100 hover:bg-gray-400 dark:bg-gray-100 dark:text-gray-900 dark:hover:bg-gray-300 truncate';

  const reset = async () => {
    await threadsStore.setSendingBlocked(false);
    fileId = '';
  };

  const handleGeneralError = async (toastData: ToastData) => {
    toastStore.addToast(toastData);
    if (fileId) {
      const fileMetadataIndex = attachedFiles.findIndex((f) => f.id === fileId);
      attachedFileMetadata[fileMetadataIndex] = {
        ...attachedFileMetadata[fileMetadataIndex],
        status: 'error',
        errorText: toastData.subtitle
      };
    }
    await reset();
  };

  const transcribeOrTranslate = async (
    fileMetadata: FileMetadata,
    method: 'translation' | 'transcription'
  ) => {
    const toastError =
      method === 'translation' ? FILE_TRANSLATION_ERROR() : FILE_TRANSCRIPTION_ERROR();

    const adjective = method === 'translation' ? ' Translate' : 'Transcribe'

    if (!fileMetadata.id) {
      await handleGeneralError(toastError);
      return;
    }
    fileId = fileMetadata.id;
    await threadsStore.setSendingBlocked(true);
    try {
      if (!threadId) {
        // create new thread
        await threadsStore.newThread(
          `${adjective} ${fileMetadata.name}`
        );
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
        disabled={fileId}
      >
        {#if fileId === file.id}
          <Spinner class="me-2" size="2" color="white" /><span
            >{`Translating ${shortenFileName(file.name)}`}</span
          >
        {:else}
          {`Translate ${shortenFileName(file.name)}`}{/if}</Button
      >
    </div>
  {/each}
  {#each audioFiles as file}
    <div in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
      <Button
        color="dark"
        class={customBtnClass}
        on:click={() => transcribeOrTranslate(file, 'transcription')}
        disabled={fileId}
      >
        {#if fileId === file.id}
          <Spinner class="me-2" size="2" color="white" /><span
            >{`Transcribing ${shortenFileName(file.name)}`}</span
          >
        {:else}
          {`Transcribe ${shortenFileName(file.name)}`}{/if}</Button
      >
    </div>
  {/each}
</div>
