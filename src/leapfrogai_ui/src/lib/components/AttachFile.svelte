<script lang="ts">
  import { Attachment } from 'carbon-icons-svelte';
  import { Button } from 'carbon-components-svelte';

  export let disabled = false;
  export let accept = ['.pdf', '.txt', '.text'];
  export let multiple = false;
  export let files: File[] = [];
  export let handleAttach: () => void;
</script>

<Button
  icon={Attachment}
  kind="ghost"
  size="small"
  iconDescription="Attach File"
  on:click={handleAttach}
/>

<input
  {disabled}
  type="file"
  tabindex="-1"
  accept={accept.join(',')}
  {multiple}
  name="files"
  class:bx--visually-hidden={true}
  {...$$restProps}
  on:change|stopPropagation={({ target }) => {
    if (target) {
      files = [...target.files];
    }
  }}
  on:click
  on:click={({ target }) => {
    if (target) {
      target.value = null;
    }
  }}
/>
