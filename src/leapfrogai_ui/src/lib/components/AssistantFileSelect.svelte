<script lang="ts">
  import { FileUploaderItem } from 'carbon-components-svelte';
  import { fade } from 'svelte/transition';
  import LFMultiSelect from '$components/LFMultiSelect.svelte';
  import { filesStore } from '$stores';
  import type { FilesForm } from '$lib/types/files';
  import { ACCEPTED_FILE_TYPES } from '$constants';

  export let filesForm: FilesForm;

  $: filteredStoreFiles = [...$filesStore.files, ...$filesStore.pendingUploads]
    .filter((f) => $filesStore.selectedAssistantFileIds.includes(f.id))
    .sort((a, b) => a.filename.localeCompare(b.filename));

  $: fileIdsWithoutErrors = $filesStore.files
    .map((row) => row.id)
    .filter((id) => $filesStore.selectedAssistantFileIds.includes(id));
</script>

<div id="multi-select-container">
  <LFMultiSelect
    label="Choose data sources"
    items={$filesStore.files.map((file) => ({ id: file.id, text: file.filename }))}
    direction="top"
    accept={ACCEPTED_FILE_TYPES}
    bind:selectedIds={$filesStore.selectedAssistantFileIds}
    {filesForm}
  />
</div>

<div class="file-item-list">
  {#each filteredStoreFiles as file}
    <div transition:fade={{ duration: 70 }}>
      <FileUploaderItem
        data-testid={`${file.filename}-${file.status}-uploader-item`}
        invalid={file.status === 'error'}
        id={file.id}
        name={file.filename}
        size="small"
        status={file.status === 'uploading' ? 'uploading' : 'edit'}
        style="max-width: 100%"
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

<style lang="scss">
  #multi-select-container {
    // remove border from first item so button outline shows instead
    :global(.bx--list-box__menu-item__option:nth-of-type(1)) {
      border-top: none;
    }
  }

  .file-item-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  :global(.bx--tag) {
    // hide tag but keep spacing for multiselect text the same
    visibility: hidden;
    width: 0rem;
    margin-left: 0.25rem;
  }
</style>
