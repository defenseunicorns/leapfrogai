<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import Filename from '$components/Filename.svelte';
  import { Card } from 'flowbite-svelte';

  export let id = 'ccs-' + Math.random().toString(36);
  export let status: 'uploading' | 'edit' | 'complete' = 'uploading';
  export let invalid = false;
  export let name = '';

  const dispatch = createEventDispatcher();
</script>

<Card {id} class="w-full " padding="xs" {...$$restProps}>
  <div class="flex items-center justify-between">
    <p class="truncate font-normal leading-tight text-gray-700 dark:text-gray-400">
      {name}
    </p>

    <Filename
      on:keydown={({ key }) => {
        if (key === ' ' || key === 'Enter') {
          dispatch('delete', id);
        }
      }}
      on:click={() => {
        dispatch('delete', id);
      }}
      {status}
      {invalid}
    />
  </div>
</Card>
