<script lang="ts">
  import { Button, Modal, P } from 'flowbite-svelte';
  import { ExclamationCircleOutline } from 'flowbite-svelte-icons';
  import { toastStore } from '$stores';
  import { page } from '$app/stores';
  import { invalidate } from '$app/navigation';
  import { createEventDispatcher } from 'svelte';

  export let confirmDeleteModalOpen: boolean;
  export let selectedRowIds: string[];
  export let deleting: boolean;

  const dispatch = createEventDispatcher();

  $: keyNames = $page.data.keys
    ? $page.data.keys
        .map((key) => {
          if (selectedRowIds.includes(key.id)) return key.name;
        })
        .filter((key) => key !== undefined)
        .join(', ')
    : '';

  const handleCancel = () => {
    confirmDeleteModalOpen = false;
  };

  const handleDelete = async () => {
    deleting = true;
    const isMultiple = selectedRowIds.length > 1;
    const res = await fetch('/api/api-keys/delete', {
      body: JSON.stringify({ ids: selectedRowIds }),
      method: 'DELETE'
    });
    dispatch('delete', selectedRowIds);
    deleting = false;
    if (res.ok) {
      toastStore.addToast({
        kind: 'success',
        title: `${isMultiple ? 'Keys' : 'Key'} Deleted`
      });
    } else {
      toastStore.addToast({
        kind: 'error',
        title: `Error Deleting ${isMultiple ? 'Keys' : 'Key'}`
      });
    }
    await invalidate('lf:api-keys');
  };
</script>

<Modal
  data-testid="delete-api-key-modal"
  bind:open={confirmDeleteModalOpen}
  autoclose
  title={`Delete API ${keyNames.length > 0 ? 'Keys' : 'Key'}`}
  on:close={handleCancel}
  color="primary"
>
  <div class="flex flex-col gap-4">
    <ExclamationCircleOutline class="mx-auto  h-12 w-12 text-gray-400 dark:text-white" />
    <P size="xl" class="text-center dark:text-gray-400">
      Are you sure you want to delete <strong>{keyNames}</strong>
    </P>
    <div class="flex justify-end gap-2">
      <Button color="alternative" on:click={handleCancel} size="sm">Cancel</Button>
      <Button color="red" on:click={handleDelete} disabled={deleting} size="sm">Delete</Button>
    </div>
  </div></Modal
>
