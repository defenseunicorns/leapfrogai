<script lang="ts">
  import { FileOutline } from 'flowbite-svelte-icons';
  import { getFileType } from '$lib/utils/files.js';
  import { Card, Spinner } from 'flowbite-svelte';

  export let name: string;
  export let type: string;
  export let loading: boolean;

  const width = 72;
</script>

<Card horizontal padding="xs" class={`w-${width}`}>
  <div class="flex gap-2">
    <div class="flex items-center rounded-lg bg-gray-700 px-2">
      {#if loading}
        <Spinner size={6} />
      {:else}
        <FileOutline size="lg" color="white" />
      {/if}
    </div>
    <h5 class="flex flex-col">
      <div
        class={`overflow-hidden text-ellipsis whitespace-nowrap text-sm font-bold text-gray-900 dark:text-white max-w-${width - 16}`}
      >
        {name}
      </div>
      <p class="text-sm font-normal text-gray-700 dark:text-gray-400">
        {getFileType(type)}
      </p>
    </h5>
  </div>
</Card>
