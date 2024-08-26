<script lang="ts">
  import UploadedFileCard from '$components/UploadedFileCard.svelte';
  import type { FileMetadata } from '$lib/types/files';

  export let attachedFileMetadata: FileMetadata[];
  export let handleRemoveFile: (id: string, index: number) => void;
</script>

<div
  id="uploaded-files"
  class={attachedFileMetadata.length > 0
    ? 'ml-9 flex max-w-full  gap-2 overflow-x-scroll bg-gray-700 px-2.5'
    : 'hidden'}
>
  {#each attachedFileMetadata as file, index}
    <UploadedFileCard
      name={file.name}
      type={file.type}
      status={file.status}
      on:delete={() => handleRemoveFile(file.id, index)}
    />
  {/each}
</div>
