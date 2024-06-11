<script lang="ts">
  import { Upload } from 'carbon-icons-svelte';
  import { ListBoxMenuItem } from 'carbon-components-svelte';
  import { createEventDispatcher } from 'svelte';
  import { fi } from '@faker-js/faker';
  import type {FileRow} from "$lib/types/files";

  export let multiple = false;
  export let files: File[] = [];
  export let labelText = 'Add file';
  export let ref: HTMLInputElement | null = null;
  export let id = 'ccs-' + Math.random().toString(36);
  export let disabled = false;
  export let tabindex = '0';
  export let role = 'button';
  export let name = '';
  export let accept: ReadonlyArray<string> = [];

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
    for(const file of files){
      const newFile: FileRow = {
        id: `${file.name}-${new Date()}`, // temp id
        filename: file.name,
        status: 'uploading',
        created_at: null
      };
    }
  }

  // The parent ListBox that uses this component has on:click|preventDefault for the other
  // items in the list box to prevent it from closing. We get around that with this function
  // to ensure you can still open a file upload dialog.
  const handleClick = (e: MouseEvent) => {
    e.stopPropagation();
    if (ref) {
      ref.click();
    }
  };
</script>

<div class="file-upload-container">
  <ListBoxMenuItem on:click={handleClick}>
    <label
      for={id}
      aria-disabled={disabled}
      tabindex={disabled ? '-1' : tabindex}
      on:keydown
      on:keydown={({ key }) => {
        if (key === ' ' || key === 'Enter') {
          ref.click();
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
      {name}
      class:bx--visually-hidden={true}
      {...$$restProps}
      on:change|stopPropagation={({ target }) => {
        if (target) {
          files = [...target.files];
          labelText = files.length > 1 ? `${files.length} files` : files[0].name;
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
</div>

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
