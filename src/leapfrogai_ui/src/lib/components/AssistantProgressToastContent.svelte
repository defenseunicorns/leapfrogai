<script lang="ts">
  import { Spinner } from 'flowbite-svelte';
  import { browser } from '$app/environment';
  import { filesStore, toastStore } from '$stores';
  import { CheckOutline, CloseCircleOutline } from 'flowbite-svelte-icons';

  export let toastId: string;
  export let vectorStoreId: string;

  let vector_store_file_ids: string[] = [];
  let checkingStatus = true;

  $: filesToDisplay = $filesStore.files.filter((file) => vector_store_file_ids.includes(file.id));
  $: allCompleted =
    filesToDisplay.length > 0 && filesToDisplay.every((item) => item.vectorStatus === 'completed');
  $: console.log('allCompleted', allCompleted);
  $: console.log('filesToDisplay', filesToDisplay);

  const setVectorStoreFileIds = () => {
    setTimeout(async () => {
      const res = await fetch(`/api/vector-store-files?id=${vectorStoreId}`);
      if (res.ok) {
        const data = await res.json();
        vector_store_file_ids = data?.data?.map((file) => file.id);
      }
      checkingStatus = false;
    }, 3000);
  };
  $: if (browser && vectorStoreId) {
    setVectorStoreFileIds();
  }

  $: if (allCompleted) {
    setTimeout(() => {
      toastStore.dismissToast(toastId);
    }, 5000);
  }
</script>

<div class="flex max-h-36 flex-col overflow-y-auto">
  {#if checkingStatus}
    <div>Fetching status...</div>
  {:else if allCompleted}
    <div class="text-green-500">File Processing Complete</div>
  {:else}
    {#each filesToDisplay as file}
      <div class="flex items-center justify-between py-1">
        <div>{file?.filename}</div>

        {#if file?.vectorStatus === 'in_progress'}
          <Spinner
            data-testid={`file-${file.id}-vector-in-progress`}
            class="me-3"
            size="4"
            color="white"
          />
        {:else if file?.vectorStatus === 'completed'}
          <CheckOutline
            data-testid={`file-${file.id}-vector-completed`}
            color="green"
            class="me-2"
          />
        {:else if file?.vectorStatus === 'failed' || file?.status === 'cancelled'}
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
