<script lang="ts">
  import { FileUploaderItem } from 'carbon-components-svelte';
  import { fade } from 'svelte/transition';
  import LFMultiSelect from '$components/LFMultiSelect.svelte';
  import { filesStore } from '$stores';
  import type { FilesForm } from '$lib/types/files';

  export let filesForm: FilesForm;

  // Files with errors remain selected for 1.5 seconds until the files are re-fetched do show the error state
  // If the assistant is saved before they are re-fetched, we need to ensure any files with errors are removed
  // from the list of ids being saved
  $: fileIdsWithoutErrors = $filesStore.files
    .filter((row) => row.status !== 'error')
    .map((row) => row.id)
    .filter((id) => $filesStore.selectedAssistantFileIds.includes(id));
</script>

<div id="multi-select-container">
  <LFMultiSelect
    label="Choose data sources"
    items={$filesStore.files.map((file) => ({ id: file.id, text: file.filename }))}
    direction="top"
    accept={['.pdf', 'txt']}
    bind:selectedIds={$filesStore.selectedAssistantFileIds}
    {filesForm}
  />
</div>

<div class="file-item-list">
  {#each $filesStore.files
    .filter((f) => $filesStore.selectedAssistantFileIds.includes(f.id))
    .sort((a, b) => a.filename.localeCompare(b.filename)) as file}
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
    gap: layout.$spacing-03;
  }

  :global(.bx--tag) {
    // hide tag but keep spacing for multiselect text the same
    visibility: hidden;
    width: 0rem;
    margin-left: 0.25rem;
  }
</style>
