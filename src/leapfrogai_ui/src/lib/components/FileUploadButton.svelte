<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { ActionResult } from '@sveltejs/kit';
  import { superForm } from 'sveltekit-superforms';
  import { Button } from 'flowbite-svelte';
  import { yup } from 'sveltekit-superforms/adapters';
  import { filesSchema } from '$schemas/files';
  import { filesStore, toastStore } from '$stores';
  import type { FilesForm } from '$lib/types/files';

  export let multiple = false;
  export let files: File[] = [];
  export let labelText = 'Add file';
  export let ref: HTMLInputElement | null = null;
  export let id = 'ccs-' + Math.random().toString(36);
  export let disabled = false;
  export let accept: ReadonlyArray<string> = [];
  export let disableLabelChanges = false;

  export let filesForm: FilesForm; // for the form
  export let open: boolean; //Parent MultiFileSelect open reactive variable

  let initialLabelText = labelText;

  const dispatch = createEventDispatcher();

  $: if (ref && files.length === 0) {
    labelText = initialLabelText;
    ref.value = '';
  }

  $: if (files.length > 0) {
    handleUpload();
  }

  const handleUpload = () => {
    open = false; // close parent multi select
    filesStore.setUploading(true);
    filesStore.addUploadingFiles(files, { autoSelectUploadedFiles: true });
    submit();
  };

  const handleResult = async (result: ActionResult) => {
    if (result.type === 'success') {
      const idsToSelect: string[] = [];
      const uploadedFiles = result.data?.uploadedFiles;
      filesStore.updateWithUploadResults(result.data?.uploadedFiles);
      for (const uploadedFile of uploadedFiles) {
        idsToSelect.push(uploadedFile.id);
      }
      filesStore.addSelectedAssistantFileIds(idsToSelect);
    }
    filesStore.setUploading(false);
  };

  const { enhance, submit } = superForm(filesForm, {
    validators: yup(filesSchema),
    invalidateAll: false,
    onError() {
      // Backend failure, not just a single file failure
      filesStore.setAllUploadingToError();
      toastStore.addToast({
        kind: 'error',
        title: 'Upload Failed',
        subtitle: `Please try again or contact support`
      });
    },
    onResult: async ({ result }) => handleResult(result)
  });
</script>

<form
  class="file-upload-container"
  method="POST"
  enctype="multipart/form-data"
  use:enhance
  action="/chat/file-management"
>
  <Button on:click={() => ref?.click()} {disabled}>
    {labelText}
  </Button>
  <input
    {id}
    bind:this={ref}
    {disabled}
    type="file"
    tabindex="-1"
    {accept}
    {multiple}
    name="files"
    class="sr-only"
    {...$$restProps}
    on:change|stopPropagation={({ target }) => {
      if (target) {
        files = [...target.files];
        if (files && !disableLabelChanges) {
          labelText = files.length > 1 ? `${files.length} files` : files[0].name;
        }
        dispatch('change', files);
      }
    }}
    on:click
    on:click={({ target }) => {
      if (target) {
        target.value = null;
      }
    }}
  />
</form>
