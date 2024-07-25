<script lang="ts">
  import {
    Button,
    DataTable,
    Loading,
    Toolbar,
    ToolbarBatchActions,
    ToolbarContent,
    ToolbarSearch
  } from 'carbon-components-svelte';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { formatDate } from '$helpers/dates';
  import { Add, TrashCan } from 'carbon-icons-svelte';
  import { toastStore } from '$stores';
  import { newAPIKeySchema } from '$schemas/apiKey.js';
  import { invalidate } from '$app/navigation';
  import type { APIKeyRow } from '$lib/types/apiKeys';
  import { formatKeyShort } from '$helpers/apiKeyHelpers';
  import CreateApiKeyModal from '$components/modals/CreateApiKeyModal.svelte';
  import DeleteApiKeyModal from '$components/modals/DeleteApiKeyModal.svelte';
  import SaveApiKeyModal from '$components/modals/CopyApiKeyModal.svelte';

  export let data;

  let selectedRowIds: string[] = [];
  let filteredRowIds: string[] = [];
  let modalOpen = false;
  let confirmDeleteModalOpen = false;
  let copyKeyModalOpen = false;
  let deleting = false;
  let selectedExpirationIndex = 1;
  let selectedExpirationDate: number;
  let createdKey: APIKeyRow | null = null;

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
  $: active = selectedRowIds.length > 0;
  $: keyNames = data.keys
    ? data.keys
        .map((key) => {
          if (selectedRowIds.includes(key.id)) return key.name;
        })
        .filter((key) => key !== undefined)
        .join(', ')
    : '';

  const handleError = () => {
    modalOpen = false;
    toastStore.addToast({
      kind: 'error',
      title: 'Creation Failed'
    });
    invalidate('lf:api-keys');
  };

  const { form, errors, enhance, submit, reset } = superForm(data.form, {
    invalidateAll: false,
    validators: yup(newAPIKeySchema),
    onError() {
      handleError();
    },
    onResult({ result }) {
      if (result.type === 'success') {
        createdKey = result.data?.key;
        modalOpen = false;
        copyKeyModalOpen = true;
        toastStore.addToast({
          kind: 'success',
          title: 'Created Successfully',
          subtitle: `${result.data?.form.data.name} created successfully.`
        });
        invalidate('lf:api-keys');
      }
    }
  });

  const handleCancel = () => {
    modalOpen = false;
    reset();
  };

  const handleDelete = async () => {
    deleting = true;
    const isMultiple = selectedRowIds.length > 1;
    const res = await fetch('/api/api-keys/delete', {
      body: JSON.stringify({ ids: selectedRowIds }),
      method: 'DELETE'
    });
    confirmDeleteModalOpen = false;
    selectedRowIds = [];
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

  const handleCancelConfirmDelete = () => {
    confirmDeleteModalOpen = false;
    selectedRowIds = [];
    active = false;
  };

  const handleCloseCopyKeyModal = () => {
    copyKeyModalOpen = false;
    createdKey = null;
  };
</script>

<div class="container">
  <div class="centered-spaced-container">
    <div class="title">API Keys</div>
  </div>
  <form method="POST" enctype="multipart/form-data" use:enhance>
    <DataTable
      bind:selectedRowIds
      headers={[
        { key: 'name', value: 'Name', display: (name) => name || '' },
        { key: 'api_key', value: 'Secret Keys', display: (key) => formatKeyShort(key) },
        {
          key: 'created_at',
          value: 'Created',
          display: (created_at) => formatDate(new Date(created_at))
        },
        {
          key: 'expires_at',
          value: 'Expires',
          display: (created_at) => formatDate(new Date(created_at))
        },
        { key: 'permissions', value: 'Permissions', display: (permissions) => permissions || '' }
      ]}
      rows={data.keys || []}
      batchSelection={true}
      sortable
    >
      <Toolbar>
        <ToolbarBatchActions
          bind:active
          on:cancel={(e) => {
            e.preventDefault();
            active = false;
            selectedRowIds = [];
          }}
        >
          {#if deleting}
            <div class="deleting">
              <Loading withOverlay={false} small data-testid="delete-pending" />
            </div>
          {:else}
            <Button
              icon={TrashCan}
              on:click={() => (confirmDeleteModalOpen = true)}
              disabled={selectedRowIds.length === 0}>Delete</Button
            >
          {/if}</ToolbarBatchActions
        >
        <ToolbarContent>
          <ToolbarSearch
            bind:filteredRowIds
            shouldFilterRows={(row, value) => {
              // filter for name and date
              const formattedCreatedAtDate = formatDate(new Date(row.created_at)).toLowerCase();
              const formattedExpiresAtDate = formatDate(new Date(row.expires_at)).toLowerCase();
              return (
                row.name?.toLowerCase().includes(value.toString().toLowerCase()) ||
                row.api_key.toLowerCase().includes(value.toString().toLowerCase()) ||
                formattedCreatedAtDate.includes(value.toString().toLowerCase()) ||
                formattedExpiresAtDate.includes(value.toString().toLowerCase()) ||
                row.permissions?.toLowerCase().includes(value.toString().toLowerCase())
              );
            }}
          />
          <Button
            icon={Add}
            on:click={() => {
              modalOpen = true;
            }}>Create new</Button
          >
        </ToolbarContent>
      </Toolbar>
    </DataTable>
    <CreateApiKeyModal
      {modalOpen}
      {handleCancel}
      {submit}
      bind:name={$form.name}
      bind:selectedExpirationIndex
      bind:selectedExpirationDate
      invalidText={$errors.name?.toString()}
    />
  </form>

  <DeleteApiKeyModal
    {confirmDeleteModalOpen}
    {keyNames}
    {deleting}
    {handleCancelConfirmDelete}
    {handleDelete}
  />
  <SaveApiKeyModal {copyKeyModalOpen} {handleCloseCopyKeyModal} {createdKey} />
</div>

<style lang="scss">
  .container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0 12rem 0 12rem;
  }

  .centered-spaced-container {
    display: flex;
    gap: 1.5rem;
    align-items: center;
  }

  .title {
    font-size: 2rem;
    line-height: 2.5rem;
    font-weight: 400;
    letter-spacing: 0px;
  }

  .deleting {
    margin-right: 1rem;
  }
</style>
