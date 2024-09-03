<script lang="ts">
  import { Spinner } from 'flowbite-svelte';
  import { filesStore, toastStore } from '$stores';
  import { CheckOutline, ClockOutline, CloseCircleOutline } from 'flowbite-svelte-icons';
  import { createEventDispatcher } from 'svelte';
  import vectorStatusStore from '$stores/vectorFilesStore';

  export let toastId: string;
  export let vectorStoreId: string;
  export let fileIds: string[];

  const dispatch = createEventDispatcher();

  $: filesToDisplay = $filesStore.files.filter((file) => fileIds.includes(file.id));

  $: allCompleted =
    filesToDisplay.length > 0 &&
    filesToDisplay.every(
      (file) =>
        $vectorStatusStore[file.id] && $vectorStatusStore[file.id][vectorStoreId] === 'completed'
    );

  $: errorStatus = filesToDisplay.some(
    (file) => $vectorStatusStore[file.id] && $vectorStatusStore[file.id][vectorStoreId] === 'failed'
  );

  $: if (allCompleted) {
    dispatch('statusChange', 'success');
    setTimeout(() => {
      toastStore.dismissToast(toastId);
    }, 5000);
  }

  $: if (errorStatus) {
    dispatch('statusChange', 'error');
  }
</script>

<div class="flex max-h-36 flex-col overflow-y-auto">
  {#if allCompleted}
    <div class="text-green-500">File Processing Complete</div>
  {:else}
    {#each filesToDisplay as file}
      <div class="flex items-center justify-between py-1">
        <div class="max-w-32 truncate">{file?.filename}</div>

        {#if !$vectorStatusStore[file.id] || !$vectorStatusStore[file.id][vectorStoreId]}
          <ClockOutline
            data-testid={`file-${file.id}-vector-pending`}
            color="orange"
            class="me-2"
          />
        {:else if $vectorStatusStore[file.id][vectorStoreId] === 'in_progress'}
          <Spinner
            data-testid={`file-${file.id}-vector-in-progress`}
            class="me-3"
            size="4"
            color="white"
          />
        {:else if $vectorStatusStore[file.id][vectorStoreId] === 'completed'}
          <CheckOutline
            data-testid={`file-${file.id}-vector-completed`}
            color="green"
            class="me-2"
          />
        {:else if $vectorStatusStore[file.id][vectorStoreId] === 'failed' || $vectorStatusStore[file.id][vectorStoreId] === 'cancelled'}
          <CloseCircleOutline
            data-testid={`file-${file.id}-vector-in-failed`}
            color="red"
            class="me-2"
          />
        {/if}
      </div>
    {/each}
  {/if}
</div>
