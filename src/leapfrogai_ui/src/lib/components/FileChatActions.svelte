<script lang="ts">
  import { Button, Spinner } from 'flowbite-svelte';
  import { shortenFileName } from '$helpers/stringHelpers';
  import { saveMessage } from '$helpers/chatHelpers';
  import type { FileMetadata, LFFile } from '$lib/types/files';
  import { threadsStore, toastStore } from '$stores';
  import { FILE_TRANSLATION_ERROR } from '$constants/toastMessages';
  import { tick } from 'svelte';
  import { page } from '$app/stores';

  export let uploadedFiles: LFFile[];
  export let attachedFileMetadata: FileMetadata[];
  export let threadId: string;
  export let translating: boolean;

  $: audioFiles = attachedFileMetadata.filter((file) => file.type.startsWith('audio/'));

  const customBtnClass =
    'rounded text-xs px-2.5 py-0.5 text-gray-500 bg-gray-100 hover:bg-gray-400 dark:bg-gray-100 dark:text-gray-900 dark:hover:bg-gray-300 ';

  const translateFile = async (fileMetadata: FileMetadata) => {
    translating = true;
    await threadsStore.setSendingBlocked(true);
    try {
      if (!threadId) {
        // create new thread
        await threadsStore.newThread(`Translate ${fileMetadata.name}`);
        await tick(); // allow store to update
        threadId = $page.params.thread_id;
      }

      const metadataToSave = attachedFileMetadata.find((f) => f.id === fileMetadata.id);
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
      // TODO - need to add to $chatMessages?

      // translate
      const file = uploadedFiles.find((f) => f.id === fileMetadata.id);
      if (!file) throw Error('File not found');

      const formData = new FormData();
      formData.append('file', file);
      const translateRes = await fetch(`/api/audio/translation`, {
        method: 'POST',
        body: formData
      });
      const translateResJson = await translateRes.json();

      // save translation response
      const translationMessage = await saveMessage({
        thread_id: threadId,
        content: translateResJson.text,
        role: 'assistant'
      });
      await threadsStore.addMessageToStore(translationMessage);

      uploadedFiles = uploadedFiles.filter((file) => file.id !== fileMetadata.id);
      attachedFileMetadata = attachedFileMetadata.filter((file) => file.id !== fileMetadata.id);
    } catch (e) {
      console.error(e);
      toastStore.addToast(FILE_TRANSLATION_ERROR());
      await threadsStore.setSendingBlocked(false);
    }
    await threadsStore.setSendingBlocked(false);
    translating = false;
  };
</script>

<div
  id="uploaded-files-actions"
  class={audioFiles.length > 0
    ? 'ml-6 flex max-w-full  gap-2 overflow-x-auto bg-gray-700'
    : 'hidden'}
>
  {#each audioFiles as file}
    <Button
      color="dark"
      class={customBtnClass}
      on:click={() => translateFile(file)}
      disabled={translating}
    >
      {#if translating}
        <Spinner class="me-3" size="4" color="white" /><span
          >{`Translating ${shortenFileName(file.name)}`}</span
        >
      {:else}
        {`Translate ${shortenFileName(file.name)}`}{/if}</Button
    >
  {/each}
</div>
