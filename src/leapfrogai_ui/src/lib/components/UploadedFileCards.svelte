<script lang="ts">
  import UploadedFileCard from '$components/UploadedFileCard.svelte';
  import type { FileMetadata, LFFile } from '$lib/types/files';

  export let attachedFiles: LFFile[];
  export let attachedFileMetadata: FileMetadata[];

  const handleRemoveFile = (id: string) => {
    attachedFileMetadata = attachedFileMetadata.filter((file) => file.id !== id);
    attachedFiles = attachedFiles.filter((file) => file.id !== id);
  };
</script>

<div id="uploaded-files" class={attachedFileMetadata.length > 0 ? ' flex  gap-2 py-2' : 'hidden'}>
  {#each attachedFileMetadata as fileMetadata}
    <UploadedFileCard {fileMetadata} on:delete={() => handleRemoveFile(fileMetadata.id)} />
  {/each}
</div>
