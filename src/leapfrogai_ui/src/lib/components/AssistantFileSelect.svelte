<script lang="ts">
  import { FileUploaderItem } from 'carbon-components-svelte';
  import { fade } from 'svelte/transition';
  import LFMultiSelect from '$components/LFMultiSelect.svelte';
  import { filesStore } from '$stores';
  import type { FilesForm } from '$lib/types/files';

  export let filesForm: FilesForm;
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
  {#each [...$filesStore.files, ...$filesStore.pendingFiles, ...$filesStore.errorFiles]
    .filter((f) => $filesStore.selectedAssistantFileIds.includes(f.id))
    .sort((a, b) => a.filename.localeCompare(b.filename)) as file}
    <div transition:fade={{ duration: 70 }}>
      <FileUploaderItem
        id={file.id}
        name={file.filename}
        size="small"
        status="edit"
        style="max-width: 100%"
        on:delete={() => {
          filesStore.setSelectedAssistantFileIds(
            $filesStore.selectedAssistantFileIds.filter((id) => id !== file.id)
          );
        }}
      />
    </div>
  {/each}
  {#each $filesStore.pendingFiles as pendingFile}
    <div transition:fade={{ duration: 70 }}>
      <FileUploaderItem
        id={pendingFile.id}
        name={pendingFile.filename}
        size="small"
        status="uploading"
        style="max-width: 100%"
        on:delete={() => {
          filesStore.setSelectedAssistantFileIds(
            $filesStore.selectedAssistantFileIds.filter((id) => id !== pendingFile.id)
          );
        }}
      />
    </div>
  {/each}
  {#each $filesStore.errorFiles as errorFile}
    <div transition:fade={{ duration: 70 }}>
      <FileUploaderItem
        invalid
        id={errorFile.id}
        name={errorFile.filename}
        size="small"
        status="uploading"
        style="max-width: 100%"
        on:delete={() => {
          filesStore.setSelectedAssistantFileIds(
            $filesStore.selectedAssistantFileIds.filter((id) => id !== errorFile.id)
          );
        }}
      />
    </div>
  {/each}
</div>

<input type="hidden" name="data_sources" bind:value={$filesStore.selectedAssistantFileIds} />

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
