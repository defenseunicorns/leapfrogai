<!--This is a custom version of Carbon Components Svelte's FileUploaderButton to support usage of an inline icon-->

<script lang="ts">
  import { Download } from 'carbon-icons-svelte';
  import { Button } from 'carbon-components-svelte';

  export let importing: boolean;

  /** Obtain a reference to the input HTML element */
  export let ref: HTMLInputElement | null = null;
  export let accept: string[] = [];
  export let onUpload: (files: FileList) => void;

  let files: FileList;

  $: if (files) {
    onUpload(files);
  }
</script>

<div>
  <input
    data-testid="import data input"
    id="import-conversations"
    bind:this={ref}
    type="file"
    accept={accept.join(',')}
    multiple={false}
    name="import"
    on:keydown={({ key }) => {
      if (key === ' ' || key === 'Enter') {
        ref?.click();
      }
    }}
    bind:files
    class:bx--visually-hidden={true}
  />

  <Button
    id="import-btn"
    kind="ghost"
    disabled={importing}
    icon={Download}
    iconDescription="Import conversations"
    on:click={() => ref?.click()}>Import data</Button
  >
</div>
