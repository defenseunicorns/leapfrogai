<script lang="ts">
  import { fade } from 'svelte/transition';
  import { CloseOutline, FileOutline } from 'flowbite-svelte-icons';
  import { getFileType } from '$lib/utils/files.js';
  import { Card, Spinner, ToolbarButton } from 'flowbite-svelte';
  import { createEventDispatcher } from 'svelte';

  export let name: string;
  export let type: string;
  export let status: boolean;
  export let disableDelete = false;

  const dispatch = createEventDispatcher();

  $: hovered = false;
</script>

<div in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
  <Card
    id="card"
    horizontal
    padding="xs"
    class="w-72 min-w-72 bg-gray-800"
    on:mouseenter={() => (hovered = true)}
    on:mouseleave={() => (hovered = false)}
  >
    <div class="flex w-full flex-row items-center justify-between">
      <div class="flex gap-2">
        <div class="flex items-center rounded-lg bg-gray-700 px-2">
          {#if status === 'uploading'}
            <Spinner size={6} />
          {:else}
            <FileOutline size="lg" color="white" />
          {/if}
        </div>
        <h5 class="flex flex-col">
          <div
            class={`max-w-48 overflow-hidden text-ellipsis whitespace-nowrap text-sm font-bold text-gray-900 dark:text-white `}
          >
            {name}
          </div>
          <p class="text-sm font-normal text-gray-700 dark:text-gray-400">
            {getFileType(type)}
          </p>
        </h5>
      </div>
      {#if hovered && !disableDelete}
        <ToolbarButton on:click={() => dispatch('delete')}>
          <CloseOutline />
        </ToolbarButton>
      {/if}
    </div>
  </Card>
</div>
