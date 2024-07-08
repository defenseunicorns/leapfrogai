<script lang="ts">
  import { ContentSwitcher, Modal, Switch, TextInput } from 'carbon-components-svelte';

  export let modalOpen: boolean;
  export let handleCancel: () => void;
  export let submit: () => void;
  export let name: string;
  export let invalidText: string | undefined;
  export let selectedExpirationIndex: number;
  export let selectedExpirationDate: number;
</script>

<Modal
  bind:open={modalOpen}
  preventCloseOnClickOutside
  modalHeading="Create new secret key"
  primaryButtonText="Create"
  secondaryButtonText="Cancel"
  hasForm
  on:click:button--secondary={handleCancel}
  on:close={handleCancel}
  on:submit={submit}
>
  <div class="modal-inner-content">
    <p style="width: 70%;">
      This API key is linked to your user account and gives full access to it. Please be careful and
      keep it secret.
    </p>

    <TextInput
      id="name"
      name="name"
      labelText="Name"
      placeholder="Test Key"
      size="sm"
      autocomplete="off"
      bind:value={name}
      invalid={!!invalidText}
      {invalidText}
    />
    <div>
      <label for="expiration" class:bx--label={true}>Expiration</label>
      <ContentSwitcher
        id="expiration"
        size="xl"
        style="width: 60%"
        bind:selectedIndex={selectedExpirationIndex}
      >
        <Switch text="7 Days" />
        <Switch text="30 Days" />
        <Switch text="60 Days" />
        <Switch text="90 Days" />
      </ContentSwitcher>
    </div>
    <input type="hidden" name="expires_at" value={selectedExpirationDate} />
  </div>
</Modal>

<style lang="scss">
  .modal-inner-content {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-06;
  }
</style>
