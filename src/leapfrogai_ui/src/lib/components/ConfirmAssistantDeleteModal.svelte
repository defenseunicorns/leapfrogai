<script lang="ts">
  import { Modal } from 'carbon-components-svelte';
  import type { Assistant } from 'openai/resources/beta/assistants';
  import { filesStore } from '$stores';

  export let open: boolean;
  export let affectedAssistantsLoading: boolean;
  export let deleting: boolean;
  export let confirmDeleteModalOpen: boolean;
  export let handleConfirmedDelete: () => void;
  export let affectedAssistants: Assistant[];

  const handleCancel = () => {
    confirmDeleteModalOpen = false;
    affectedAssistants = [];
    affectedAssistantsLoading = false;
  };

  $: fileNames = $filesStore.files
    .map((file) => {
      if ($filesStore.selectedFileManagementFileIds.includes(file.id)) return file.filename;
    })
    .filter((filename) => filename !== undefined)
    .join(', ');
</script>

<Modal
  danger
  bind:open
  modalHeading="Delete File"
  shouldSubmitOnEnter={false}
  primaryButtonText="Delete"
  secondaryButtonText="Cancel"
  primaryButtonDisabled={affectedAssistantsLoading || deleting}
  on:click:button--secondary={handleCancel}
  on:close={handleCancel}
  on:submit={() => handleConfirmedDelete()}
>
  {#if affectedAssistantsLoading}
    <p>Checking for any assistants affected by deletion...</p>
  {:else}
    <p>
      Are you sure you want to delete <span style="font-weight: bold">{fileNames}</span>?
      {#if affectedAssistants.length > 0}
        This will affect the following assistants:
        {#each affectedAssistants as affectedAssistant}
          <li>{affectedAssistant.name}</li>
        {/each}
      {/if}
    </p>
  {/if}
</Modal>
