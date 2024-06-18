<script lang="ts">
  import { Upload } from 'carbon-icons-svelte';
  import { ListBoxMenuItem } from 'carbon-components-svelte';
  import { createEventDispatcher } from 'svelte';
  import type { FilesForm } from '$lib/types/files';
  import { filesStore, toastStore } from '$stores';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { filesSchema } from '$schemas/files';
  import type { ActionResult } from '@sveltejs/kit';

  export let multiple = false;
  export let files: File[] = [];
  export let labelText = 'Add file';
  export let ref: HTMLInputElement | null = null;
  export let id = 'ccs-' + Math.random().toString(36);
  export let disabled = false;
  export let tabindex = '0';
  export let role = 'button';
  export let accept: ReadonlyArray<string> = [];
  export let disableLabelChanges = false;

  export let filesForm: FilesForm; // for the form
  export let open: boolean; //Parent LFMultiSelect open reactive variable

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

  // The parent ListBox that uses this component has on:click|preventDefault for the other
  // items in the list box to prevent it from closing. We get around that with this function
  // to ensure you can still open a file upload dialog.
  const handleClick = (e: MouseEvent) => {
    e.stopPropagation();
    if (ref) {
      ref.click();
    }
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
  <ListBoxMenuItem on:click={handleClick}>
    <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
    <label
      for={id}
      aria-disabled={disabled}
      tabindex={disabled ? '-1' : tabindex}
      on:keydown
      on:keydown={({ key }) => {
        if (key === ' ' || key === 'Enter') {
          ref?.click();
        }
      }}
    >
      <span {role}>
        <slot name="labelText">
          <div class="upload-item">
            <div class="upload-icon">
              <Upload />
            </div>
            <span class="bx--checkbox-label-text">{labelText}</span>
          </div>
        </slot>
      </span>
    </label>
    <input
      bind:this={ref}
      {disabled}
      type="file"
      tabindex="-1"
      {accept}
      {multiple}
      name="files"
      class:bx--visually-hidden={true}
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
  </ListBoxMenuItem>
</form>

<style lang="scss">
  .file-upload-container {
    outline: 1px solid themes.$border-subtle-03;
  }

  .upload-item {
    display: flex;
    align-items: center;
    cursor: pointer;
  }

  .upload-icon {
    display: flex;
    width: 1.4rem;
    justify-content: center;
    margin-right: 0.3rem;
  }
</style>
