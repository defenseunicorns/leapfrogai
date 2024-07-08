<script lang="ts">
  import { Modal } from 'carbon-components-svelte';

  export let confirmDeleteModalOpen: boolean;
  export let keyNames: string;
  export let deleting: boolean;
  export let handleCancelConfirmDelete: () => void;
  export let handleDelete: () => void;
</script>

<Modal
  danger
  bind:open={confirmDeleteModalOpen}
  modalHeading={`Delete API ${keyNames.length > 0 ? 'Keys' : 'Key'}`}
  primaryButtonText="Delete"
  secondaryButtonText="Cancel"
  primaryButtonDisabled={deleting}
  on:click:button--secondary={() => handleCancelConfirmDelete()}
  on:close={() => handleCancelConfirmDelete()}
  on:submit={() => handleDelete()}
>
  <p>Are you sure you want to delete <span style="font-weight: bold">{keyNames}</span>?</p>
</Modal>
