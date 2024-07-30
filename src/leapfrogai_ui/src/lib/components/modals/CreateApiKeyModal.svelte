<script lang="ts">
  import { Button, ButtonGroup, Input, Label, Modal, P } from 'flowbite-svelte';
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
    data-testid="create-api-key-modal"
    bind:open={createApiKeyModalOpen}
    autoclose
    title="Create new secret key"
    on:close={handleClose}
    color="primary"
  >
    <div class="flex flex-col gap-4">
      <div>
        <P class="dark:text-gray-400">
          This API key is linked to your user account and gives full access to it. Please be careful
          and keep it secret.
        </P>
      </div>
      <div>
        <Label for="name" class="mb-2">Name</Label>
        <Input
          name="name"
          type="text"
          placeholder="Test key"
          autocomplete="off"
          bind:value={$sForm.name}
        />
      </div>
      <div>
        <Label for="expiration" class="mb-2">Expiration</Label>
        <ButtonGroup>
          <Button
            class={selectedExpirationIndex === 0 && 'z-10 ring-2 !ring-primary-700'}
            on:click={(e) => handleExpirationClick(0, e)}>7 Days</Button
          >
          <Button
            class={selectedExpirationIndex === 1 && 'z-10 ring-2 !ring-primary-700'}
            on:click={(e) => handleExpirationClick(1, e)}>30 Days</Button
          >
          <Button
            on:click={(e) => handleExpirationClick(2, e)}
            class={selectedExpirationIndex === 2 && 'z-10 ring-2 !ring-primary-700'}>60 Days</Button
          >
          <Button
            on:click={(e) => handleExpirationClick(3, e)}
            class={selectedExpirationIndex === 3 && 'z-10 ring-2 !ring-primary-700'}>90 Days</Button
          >
        </ButtonGroup>
      </div>

      <input type="hidden" name="expires_at" value={selectedExpirationDate} />
    </div>
    <div class="flex justify-end gap-2">
      <Button color="alternative" on:click={handleClose} size="sm">Cancel</Button>
      <Button on:click={submit} size="sm">Create</Button>
    </div>
  </Modal>
</form>

<CopyApiKeyModal bind:copyKeyModalOpen {createdKey} />
