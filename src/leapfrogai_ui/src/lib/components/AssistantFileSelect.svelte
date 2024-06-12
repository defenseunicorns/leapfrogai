<script lang="ts">
  import { FileUploaderItem, MultiSelect } from 'carbon-components-svelte';
  import { fade } from 'svelte/transition';
  import type { FileObject } from 'openai/resources/files';

  export let files: FileObject[];
  export let selectedFileIds: string[];
</script>

<MultiSelect
  label="Choose data sources"
  items={files?.map((file) => ({ id: file.id, text: file.filename }))}
  direction="top"
  bind:selectedIds={selectedFileIds}
/>

<div class="file-item-list">
  {#each [...(files || [])]
    .filter((f) => selectedFileIds.includes(f.id))
    .sort((a, b) => a.filename.localeCompare(b.filename)) as file}
    <div transition:fade={{ duration: 70 }}>
      <FileUploaderItem
        id={file.id}
        name={file.filename}
        size="small"
        status="edit"
        style="max-width: 100%"
        on:delete={() => {
          selectedFileIds = selectedFileIds.filter((id) => id !== file.id);
        }}
      />
    </div>
  {/each}
</div>

<input type="hidden" name="data_sources" bind:value={selectedFileIds} />

<style lang="scss">
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
