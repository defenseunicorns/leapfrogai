<script lang="ts">
  import { fade } from 'svelte/transition';
  import { CloseOutline, FileMusicOutline, FileOutline } from 'flowbite-svelte-icons';
  import { getFileType } from '$lib/utils/files.js';
  import { Card, Spinner, ToolbarButton } from 'flowbite-svelte';
  import { createEventDispatcher } from 'svelte';
  import type { FileMetadata } from '$lib/types/files';

  export let fileMetadata: FileMetadata;
  export let disableDelete = false;

  const dispatch = createEventDispatcher();

  $: hovered = false;
</script>

<div in:fade={{ duration: 150 }} out:fade={{ duration: 150 }}>
  <Card
    id="card"
    data-testid={`${fileMetadata.name}-file-uploaded-card`}
    horizontal
    padding="xs"
    class="w-80 min-w-72 border-none"
    on:mouseenter={() => (hovered = true)}
    on:mouseleave={() => (hovered = false)}
  >
    <div class="flex w-full flex-row items-center justify-between truncate">
      <div class="flex gap-2">
        <div class="flex items-center rounded-lg bg-gray-700 px-2">
          {#if fileMetadata.status === 'uploading'}
            <Spinner data-testid={`${fileMetadata.name}-uploading`} size={6} />
          {:else if fileMetadata.status === 'error'}
            <CloseOutline
              data-testid={`${fileMetadata.name}-error`}
              size="lg"
              class="text-red-400"
            />
          {:else if fileMetadata.type.startsWith('audio/')}
            <FileMusicOutline
              data-testid={`${fileMetadata.name}-uploaded`}
              size="lg"
              color="white"
            />
          {:else}
            <FileOutline data-testid={`${fileMetadata.name}-uploaded`} size="lg" color="white" />
          {/if}
        </div>
        <h5 class="flex flex-col">
          <div class={`max-w-56 truncate text-sm font-bold text-gray-900 dark:text-white `}>
            {fileMetadata.name}
          </div>

          {#if fileMetadata.status === 'error'}
            <p class="text-sm text-red-400">
              {fileMetadata.errorText}
            </p>
          {:else}
            <p class="text-sm text-gray-400">
              {getFileType(fileMetadata.type)}
            </p>
          {/if}
        </h5>
      </div>
      {#if hovered && !disableDelete && fileMetadata.status !== 'uploading'}
        <ToolbarButton size="sm" on:click={() => dispatch('delete')}>
          <CloseOutline data-testid={`${fileMetadata.name}-remove-btn`} />
        </ToolbarButton>
      {/if}
    </div>
  </Card>
</div>
