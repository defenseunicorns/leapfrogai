<script lang="ts">
  import { fade } from 'svelte/transition';
  import { filesStore } from '$stores';
  import type { FilesForm } from '$lib/types/files';
  import { ACCEPTED_DOC_TYPES, STANDARD_FADE_DURATION } from '$constants';
  import AssistantFileDropdown from '$components/AssistantFileDropdown.svelte';
  import FileUploaderItem from '$components/FileUploaderItem.svelte';

  export let filesForm: FilesForm;

  $: filteredStoreFiles = [...$filesStore.files, ...$filesStore.pendingUploads]
    .filter((f) => $filesStore.selectedAssistantFileIds.includes(f.id))
    .sort((a, b) => a.filename.localeCompare(b.filename));

  $: fileIdsWithoutErrors = $filesStore.files
    .map((row) => row.id)
    .filter((id) => $filesStore.selectedAssistantFileIds.includes(id));
</script>

<AssistantFileDropdown accept={ACCEPTED_DOC_TYPES} {filesForm} class="mb-6" />

<div class="grid grid-cols-2 gap-4">
  {#each filteredStoreFiles as file}
    <div transition:fade={{ duration: STANDARD_FADE_DURATION }}>
      <FileUploaderItem
        id={file.id}
        data-testid={`${file.filename}-${file.status}-uploader-item`}
        invalid={file.status === 'error'}
        name={file.filename}
        status={file.status === 'uploading' ? 'uploading' : 'edit'}
        on:delete={() => {
          filesStore.setSelectedAssistantFileIds(
            $filesStore.selectedAssistantFileIds.filter((id) => id !== file.id)
          );
        }}
      />
    </div>
  {/each}
</div>

<input type="hidden" name="data_sources" bind:value={fileIdsWithoutErrors} />
