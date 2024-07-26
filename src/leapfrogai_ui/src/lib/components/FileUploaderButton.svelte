<script lang="ts">
  import { Button } from 'flowbite-svelte';
  import { createEventDispatcher } from 'svelte';

  export let accept = [];
  export let files = [];
  export let multiple = false;
  export let disabled = false;
  export let disableLabelChanges = false;
  export let labelText = 'Add file';
  export let role = 'button';
  export let tabindex = '0';
  export let id = 'ccs-' + Math.random().toString(36);
  export let name = '';
  export let ref = null;

  const dispatch = createEventDispatcher();

  let initialLabelText = labelText;

  $: if (ref && files.length === 0) {
    labelText = initialLabelText;
    ref.value = '';
  }
</script>

<Button
  on:click={(e) => {
    e.stopPropagation();
    ref?.click();
  }}
  {disabled}
  tabindex={disabled ? '-1' : tabindex}
  class={$$props.class}
>
  {labelText}
</Button>
<input
  bind:this={ref}
  type="file"
  tabindex="-1"
  {accept}
  {disabled}
  {id}
  {multiple}
  {name}
  {...$$restProps}
  class="sr-only"
  on:change|stopPropagation={({ target }) => {
    files = [...target.files];

    if (files && !disableLabelChanges) {
      labelText = files.length > 1 ? `${files.length} files` : files[0].name;
    }

    dispatch('change', files);
  }}
  on:click
  on:click={({ target }) => {
    target.value = null;
  }}
/>
