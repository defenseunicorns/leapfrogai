<script lang="ts">
  import { Modal } from 'carbon-components-svelte';
  import type { Assistant } from 'openai/resources/beta/assistants';

  export let open: boolean;
  export let affectedAssistantsLoading: boolean;
  export let deleting: boolean;
  export let confirmDeleteModalOpen: boolean;
  export let handleConfirmedDelete: () => void;
  export let affectedAssistants: Assistant[];
  export let fileNames: string[];
</script>

<Modal
  danger
  bind:open
  modalHeading="Delete File"
  shouldSubmitOnEnter={false}
  primaryButtonText="Delete"
  secondaryButtonText="Cancel"
  primaryButtonDisabled={affectedAssistantsLoading || deleting}
  on:click:button--secondary={() => (confirmDeleteModalOpen = false)}
  on:submit={() => handleConfirmedDelete()}
>
  {#if affectedAssistantsLoading}
    <p>Checking for any assistants affected by deletion...</p>
  {:else}
    <p>
      Are you sure you want to delete <span style="font-weight: bold"
        >{fileNames.join(", ")}</span
      >?
      {#if affectedAssistants.length > 0}
        This will affect the following assistants:
        {#each affectedAssistants as affectedAssistant}
          <li>{affectedAssistant.name}</li>
        {/each}
      {/if}
    </p>
  {/if}
</Modal>
