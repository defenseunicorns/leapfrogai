<script lang="ts">
  import { formatKeyLong } from '$helpers/apiKeyHelpers.js';
  import { Copy } from 'carbon-icons-svelte';
  import { calculateDays, formatDate } from '$helpers/dates.js';
  import { Button, Modal, TextInput } from 'carbon-components-svelte';
  import type { APIKeyRow } from '$lib/types/apiKeys';

  export let copyKeyModalOpen: boolean;
  export let handleCloseCopyKeyModal: () => void;
  export let handleCopyKey: () => void;
  export let createdKey: APIKeyRow | null;

  let saveKeyModalRef: HTMLDivElement;
</script>

<Modal
  bind:ref={saveKeyModalRef}
  bind:open={copyKeyModalOpen}
  modalHeading="Save secret key"
  primaryButtonText="Close"
  on:close={handleCloseCopyKeyModal}
  on:submit={handleCloseCopyKeyModal}
>
  {#if createdKey}
    <div class="centered-spaced-container" style="flex-direction: column">
      <p>
        Please store this secret key in a safe and accessible place. For security purposes, it
        cannot be viewed again through your LeapfrogAI account. If you lose it, you'll need to
        create a new one.
      </p>
      <div class="centered-spaced-lg-container" style="width: 100%">
        <TextInput
          readonly
          labelText="Key"
          value={formatKeyLong(createdKey.api_key, saveKeyModalRef?.offsetWidth || 200)}
        />
        <Button kind="tertiary" icon={Copy} size="small" on:click={handleCopyKey}>Copy</Button>
      </div>
      <div style="width: 100%">
        <label for="saved-expiration" class:bx--label={true}>Expiration</label>
        <p id="saved-expiration">
          {`${calculateDays(createdKey.created_at, createdKey.expires_at)} days - ${formatDate(new Date(createdKey.expires_at * 1000))}`}
        </p>
      </div>
    </div>
  {/if}
</Modal>

<style lang="scss">
  .centered-spaced-container {
    display: flex;
    gap: layout.$spacing-06;
    align-items: center;
  }

  .centered-spaced-lg-container {
    display: flex;
    gap: layout.$spacing-07;
    align-items: center;
    :global(.bx--text-input__readonly-icon) {
      display: none;
    }
  }
</style>
