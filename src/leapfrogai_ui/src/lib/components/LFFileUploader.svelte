<!--This is a custom version of Carbon Components Svelte's FileUploaderButton to support usage of an inline icon-->

<script lang="ts">
  import { Button } from 'flowbite-svelte';
  import { UploadOutline } from 'flowbite-svelte-icons';

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
    data-testid="import-chat-history-input"
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
    class="sr-only"
  />

  <Button
    id="import-btn"
    outline
    size="sm"
    disabled={importing}
    on:click={() => ref?.click()}
    class="w-full"
  >
    <div class="flex w-full justify-between">
      Import chat history <UploadOutline />
    </div>
  </Button>
</div>
