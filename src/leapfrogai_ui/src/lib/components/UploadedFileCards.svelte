<script lang="ts">
  import UploadedFileCard from '$components/UploadedFileCard.svelte';
  import type { FileMetadata } from '$lib/types/files';

  export let attachedFileMetadata: FileMetadata[];

  const handleRemoveFile = (id: string) => {
    attachedFileMetadata = attachedFileMetadata.filter((file) => file.id !== id);
  };
</script>

<div
  id="uploaded-files"
  class={attachedFileMetadata.length > 0
    ? 'ml-6 flex max-w-full  gap-2 overflow-x-auto bg-gray-700'
    : 'hidden'}
>
  {#each attachedFileMetadata as fileMetadata}
    <UploadedFileCard {fileMetadata} on:delete={() => handleRemoveFile(fileMetadata.id)} />
  {/each}
</div>
