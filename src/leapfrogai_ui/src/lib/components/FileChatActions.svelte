<script lang="ts">
  import { Button } from 'flowbite-svelte';
  import { v4 as uuidv4 } from 'uuid';
  import { fade } from 'svelte/transition';
  import { shortenFileName } from '$helpers/stringHelpers';
  import { saveMessage } from '$helpers/chatHelpers';
  import type { FileMetadata, LFFile } from '$lib/types/files';
  import { threadsStore, toastStore } from '$stores';
  import { AUDIO_FILE_SIZE_ERROR_TOAST, FILE_TRANSLATION_ERROR } from '$constants/toastMessages';
  import { tick } from 'svelte';
  import { page } from '$app/stores';
  import type { Message } from 'ai';
  import { AUDIO_FILE_SIZE_ERROR_TEXT } from '$constants';

  export let attachedFiles: LFFile[];
  export let attachedFileMetadata: FileMetadata[];
  export let threadId: string;
  export let originalMessages: Message[];
  export let setMessages: (messages: Message[]) => void;

  let translatingId: string;

  $: audioFiles = attachedFileMetadata.filter((file) => file.type.startsWith('audio/'));

  const customBtnClass =
    'rounded text-xs px-2.5 py-0.5 text-gray-500 bg-gray-100 hover:bg-gray-400 dark:bg-gray-100 dark:text-gray-900 dark:hover:bg-gray-300 truncate';

  const reset = async () => {
    await threadsStore.setSendingBlocked(false);
    translatingId = '';
  };

  const handleTranslationError = async (toastData: ToastData) => {
    toastStore.addToast(toastData);
    if (translatingId) {
      const fileMetadataIndex = attachedFiles.findIndex((f) => f.id === translatingId);
      attachedFileMetadata[fileMetadataIndex] = {
        ...attachedFileMetadata[fileMetadataIndex],
        status: 'error',
        errorText: toastData.subtitle
      };
    }
    await reset();
  };

  const translateFile = async (fileMetadata: FileMetadata) => {
    const attachedFileMetadataCopy = [...attachedFileMetadata];
    const attachedFilesCopy = [...attachedFiles];
    // Remove the file and file metadata to hide the actions since the response will stream in this case
    attachedFiles = attachedFiles.filter((file) => file.id !== fileMetadata.id);
    attachedFileMetadata = attachedFileMetadata.filter((file) => file.id !== fileMetadata.id);

    if (!fileMetadata.id) {
      await handleTranslationError(FILE_TRANSLATION_ERROR());
      return;
    }

    translatingId = fileMetadata.id;
    await threadsStore.setSendingBlocked(true);
    try {
      if (!threadId) {
        // create new thread
        await threadsStore.newThread(`Translate ${fileMetadata.name}`);
        await tick(); // allow store to update
        threadId = $page.params.thread_id;
      }

      const metadataToSave = attachedFileMetadataCopy.find((f) => f.id === fileMetadata.id);
      if (!metadataToSave) throw Error('Error getting file metadata');
      // Save new user message
      const newMessage = await saveMessage({
        thread_id: threadId,
        content: `Translate ${fileMetadata.name}`,
        role: 'user',
        metadata: {
          filesMetadata: JSON.stringify([metadataToSave])
        }
      });
      await threadsStore.addMessageToStore(newMessage);
      threadsStore.updateMessagesState(originalMessages, setMessages, newMessage);

      const tempId = uuidv4();
      await threadsStore.addTempEmptyMessage(threadId, tempId);

      // translate
      const file = attachedFilesCopy.find((f) => f.id === fileMetadata.id);
      if (!file) {
        await handleTranslationError(FILE_TRANSLATION_ERROR());
        return;
      }
      const formData = new FormData();
      formData.append('file', file);
      const translateRes = await fetch(`/api/audio/translation`, {
        method: 'POST',
        body: formData
      });
      const translateResJson = await translateRes.json();
      if (!translateRes.ok) {
        if (translateResJson.message === `ValidationError: ${AUDIO_FILE_SIZE_ERROR_TEXT}`) {
          await handleTranslationError(AUDIO_FILE_SIZE_ERROR_TOAST());
        } else {
          await handleTranslationError(FILE_TRANSLATION_ERROR());
        }
        return;
      }

      // save translation response
      const translationMessage = await saveMessage({
        thread_id: threadId,
        content: translateResJson.text,
        role: 'assistant'
      });
      threadsStore.replaceTempMessageWithActual(threadId, tempId, translationMessage);
      threadsStore.updateMessagesState(originalMessages, setMessages, translationMessage);
    } catch {
      await handleTranslationError(FILE_TRANSLATION_ERROR());
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
        on:click={() => translateFile(file)}
        disabled={translatingId}
      >
        {`Translate ${shortenFileName(file.name)}`}</Button
      >
    </div>
  {/each}
</div>
