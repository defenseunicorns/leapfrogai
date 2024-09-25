<script lang="ts">
  import { Button, Modal, P } from 'flowbite-svelte';
  import type { Assistant } from 'openai/resources/beta/assistants';
  import { filesStore, toastStore } from '$stores';
  import { ExclamationCircleOutline } from 'flowbite-svelte-icons';
  import { createEventDispatcher } from 'svelte';
  import vectorStatusStore from '$stores/vectorStatusStore';

  export let open;
  export let affectedAssistantsLoading: boolean;
  export let deleting: boolean;
  export let affectedAssistants: Assistant[];

  $: isMultipleFiles = $filesStore.selectedFileManagementFileIds.length > 1;

  const dispatch = createEventDispatcher();

  const handleCancel = () => {
    open = false;
    affectedAssistants = [];
    affectedAssistantsLoading = false;
  };

  const handleDeleteError = () => {
    toastStore.addToast({
      kind: 'error',
      title: `Error Deleting ${isMultipleFiles ? 'Files' : 'File'}`
    });
  };

  const handleConfirmedDelete = async () => {
    deleting = true;
    try {
      const res = await fetch('/api/files/delete', {
        method: 'DELETE',
        body: JSON.stringify({ ids: $filesStore.selectedFileManagementFileIds }),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (res.ok) {
        open = false;
        for (const id of $filesStore.selectedFileManagementFileIds) {
          filesStore.removeFile(id);
        }
        vectorStatusStore.removeFiles($filesStore.selectedFileManagementFileIds);
        filesStore.setSelectedFileManagementFileIds([]);
        toastStore.addToast({
          kind: 'success',
          title: `${isMultipleFiles ? 'Files' : 'File'} Deleted`
        });
        dispatch('delete');
      } else {
        handleDeleteError();
      }
    } catch {
      handleDeleteError();
    }
    deleting = false;
  };

  $: fileNames = $filesStore.files
    .map((file) => {
      if ($filesStore.selectedFileManagementFileIds.includes(file.id)) return file.filename;
    })
    .filter((filename) => filename !== undefined)
    .join(', ');
</script>

<Modal
  data-testid="delete-files-modal"
  bind:open
  autoclose
  title="Delete File"
  on:close={handleCancel}
  color="primary"
>
  <div class="flex flex-col gap-4">
    <ExclamationCircleOutline class="mx-auto  h-12 w-12 text-gray-400 dark:text-white" />
    {#if affectedAssistantsLoading}
      <P size="xl" class="text-center dark:text-gray-400"
        >Checking for any assistants affected by deletion...</P
      >
    {:else}
      <P size="xl" class="text-center dark:text-gray-400">
        Are you sure you want to delete <span style="font-weight: bold">{fileNames}</span>?
        {#if affectedAssistants.length > 0}
          This will affect the following assistants:
          {#each affectedAssistants as affectedAssistant}
            <li>{affectedAssistant.name}</li>
          {/each}
        {/if}
      </P>
    {/if}
    <div class="flex justify-end gap-2">
      <Button color="alternative" on:click={handleCancel} size="sm">Cancel</Button>
      <Button
        color="red"
        on:click={handleConfirmedDelete}
        disabled={deleting || affectedAssistantsLoading}
        size="sm">Delete</Button
      >
    </div>
  </div>
</Modal>
