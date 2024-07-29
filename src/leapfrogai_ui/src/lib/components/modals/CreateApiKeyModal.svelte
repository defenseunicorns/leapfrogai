<script lang="ts">
  import { Button, ButtonGroup, Heading, Input, Label, Modal, P } from 'flowbite-svelte';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { newAPIKeySchema } from '$schemas/apiKey';
  import { toastStore } from '$stores';
  import { invalidate } from '$app/navigation';
  import type { APIKeyRow } from '$lib/types/apiKeys';
  import CopyApiKeyModal from '$components/modals/CopyApiKeyModal.svelte';

  export let form;
  export let createApiKeyModalOpen: boolean;

  let selectedExpirationIndex = 1;
  let selectedExpirationDate: number;
  let createdKey: APIKeyRow | null = null;
  let copyKeyModalOpen = false;

  // Set actual expiration date based on selected Switch
  $: {
    switch (selectedExpirationIndex) {
      case 0: {
        const sevenDays = new Date();
        sevenDays.setDate(sevenDays.getDate() + 7);
        selectedExpirationDate = Math.floor(sevenDays.getTime() / 1000);
        break;
      }
      case 1: {
        const thirtyDays = new Date();
        thirtyDays.setDate(thirtyDays.getDate() + 30);
        selectedExpirationDate = Math.floor(thirtyDays.getTime() / 1000);
        break;
      }
      case 2: {
        const sixtyDays = new Date();
        sixtyDays.setDate(sixtyDays.getDate() + 60);
        selectedExpirationDate = Math.floor(sixtyDays.getTime() / 1000);
        break;
      }
      case 3: {
        const ninetyDays = new Date();
        ninetyDays.setDate(ninetyDays.getDate() + 90);
        selectedExpirationDate = Math.floor(ninetyDays.getTime() / 1000);
        break;
      }
      default: {
        selectedExpirationDate = Math.floor(new Date().getTime() / 1000);
        break;
      }
    }
  }

  const handleClose = () => {
    reset();
    selectedExpirationIndex = 1;
    createApiKeyModalOpen = false;
  };

  const {
    form: sForm,
    errors,
    enhance,
    submit,
    reset
  } = superForm(form, {
    invalidateAll: false,
    validators: yup(newAPIKeySchema),
    onError() {
      createApiKeyModalOpen = false;
      toastStore.addToast({
        kind: 'error',
        title: 'Creation Failed'
      });
      invalidate('lf:api-keys');
    },
    onResult({ result }) {
      if (result.type === 'success') {
        createdKey = result.data?.key;
        copyKeyModalOpen = true;
        handleClose();
        toastStore.addToast({
          kind: 'success',
          title: 'Created Successfully',
          subtitle: `${result.data?.form.data.name} created successfully.`
        });
        invalidate('lf:api-keys');
      }
    }
  });

  const handleExpirationClick = (index: number, e) => {
    e.stopPropagation();
    selectedExpirationIndex = index;
  };
</script>

<form method="POST" enctype="multipart/form-data" action={'/chat/api-keys'} use:enhance>
  <Modal
    bind:open={createApiKeyModalOpen}
    autoclose
    title="Create new secret key"
    on:close={handleClose}
  >
    <div class="flex flex-col gap-4">
      <div>
        <P size="xl" class="text-center">
          This API key is linked to your user account and gives full access to it.
        </P>
        <P size="xl" class="text-center">Please be careful and keep it secret.</P>
      </div>
      <div>
        <Label for="name" class="mb-2">Name</Label>
        <Input
          name="name"
          type="text"
          size="sm"
          placeholder="Test Key"
          autocomplete="off"
          invalid={$errors.name}
          bind:value={$sForm.name}
        />
        {#if $errors.name}
          <span style="color: red">{$errors.name}</span>
        {/if}
      </div>
      <div>
        <Label for="expiration" class="mb-2">Expiration</Label>
        <ButtonGroup>
          <Button
            checked={selectedExpirationIndex === 0}
            on:click={(e) => handleExpirationClick(0, e)}>7 Days</Button
          >
          <Button
            checked={selectedExpirationIndex === 1}
            on:click={(e) => handleExpirationClick(1, e)}>30 Days</Button
          >
          <Button
            checked={selectedExpirationIndex === 2}
            on:click={(e) => handleExpirationClick(2, e)}>60 Days</Button
          >
          <Button
            checked={selectedExpirationIndex === 3}
            on:click={(e) => handleExpirationClick(3, e)}>90 Days</Button
          >
        </ButtonGroup>
      </div>

      <input type="hidden" name="expires_at" value={selectedExpirationDate} />
    </div>
    <div class="flex justify-end gap-2">
      <Button color="alternative" on:click={handleClose}>Cancel</Button>
      <Button on:click={submit}>Create</Button>
    </div>
  </Modal>
</form>

<CopyApiKeyModal bind:copyKeyModalOpen {createdKey} />
