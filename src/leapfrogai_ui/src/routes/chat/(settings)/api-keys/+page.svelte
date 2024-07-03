<script lang="ts">
  import {
    Button,
    ContentSwitcher,
    DataTable,
    Loading,
    Modal,
    Switch,
    TextInput,
    Tile,
    Toolbar,
    ToolbarBatchActions,
    ToolbarContent,
    ToolbarSearch
  } from 'carbon-components-svelte';
  import { fade } from 'svelte/transition';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { formatDate } from '$helpers/dates';
  import { Add, Copy, TrashCan } from 'carbon-icons-svelte';
  import { toastStore } from '$stores';
  import { newAPIKeySchema } from '$schemas/apiKey.js';
  import { invalidate } from '$app/navigation';

  export let data;

  let selectedRowIds: string[] = [];
  let filteredRowIds: string[] = [];
  let modalOpen = false;
  let confirmDeleteModalOpen = false;
  let deleting = false;
  let selectedExpirationIndex = 1;
  let selectedExpirationDate: number;
  let createdKey: string | null = null;

  $: {
    switch (selectedExpirationIndex) {
      case 0:
        const sevenDays = new Date();
        sevenDays.setDate(sevenDays.getDate() + 7);
        selectedExpirationDate = sevenDays.getTime();
        break;
      case 1:
        const thirtyDays = new Date();
        thirtyDays.setDate(thirtyDays.getDate() + 30);
        selectedExpirationDate = thirtyDays.getTime();
        break;
      case 2:
        const sixtyDays = new Date();
        sixtyDays.setDate(sixtyDays.getDate() + 60);
        selectedExpirationDate = sixtyDays.getTime();
        break;
      case 3:
        const ninetyDays = new Date();
        ninetyDays.setDate(ninetyDays.getDate() + 90);
        selectedExpirationDate = ninetyDays.getTime();
        break;
      default:
        selectedExpirationDate = new Date().getTime();
        break;
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

  const { form, errors, enhance, submit, reset } = superForm(data.form, {
    invalidateAll: false,
    validators: yup(newAPIKeySchema),
    onError() {
      modalOpen = false;
      toastStore.addToast({
        kind: 'error',
        title: 'Error creating API Key',
        subtitle: ''
      });
      invalidate('lf:api-keys');
    },
    onResult({ result }) {
      if (result.type === 'success') {
        createdKey = result.data?.key;
        modalOpen = false;
        toastStore.addToast({
          kind: 'success',
          title: 'API key created',
          subtitle: ''
        });
        invalidate('lf:api-keys');
      }
    }
  });

  // Keys returned from the API list call should already be masked for security
  // We use this to mask the created key before the user copies it
  const formatKey = (key: string) => {
    const firstTwo = key.slice(0, 5);
    const lastFour = key.slice(-4);
    return `${firstTwo}...${lastFour}`;
  };

  const handleCancel = () => {
    modalOpen = false;
    reset();
  };

  const handleSubmit = () => {
    submit();
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
        title: `${isMultiple ? 'Keys' : 'Key'} Deleted`,
        subtitle: ''
      });
      await invalidate('lf:api-keys');
    } else {
      toastStore.addToast({
        kind: 'error',
        title: `Error Deleting ${isMultiple ? 'Keys' : 'Key'}`,
        subtitle: ''
      });
    }
  };

  const handleCancelConfirmDelete = () => {
    confirmDeleteModalOpen = false;
    selectedRowIds = [];
    active = false;
  };

  const handleCopyKey = async () => {
    if (createdKey) {
      await navigator.clipboard.writeText(createdKey);
      toastStore.addToast({
        kind: 'info',
        title: 'API Key Copied',
        subtitle: ''
      });
      createdKey = null;
    }
  };
</script>

<div class="container">
  <div class="centered-spaced-container">
    <div class="title">API Keys</div>
    {#if createdKey}
      <div class="centered-spaced-container" transition:fade={{ duration: 70 }}>
        <p>New Key:</p>
        <span
          ><div class="key-container">
            {formatKey(createdKey)}
            <button
              data-testid="copy btn"
              class="highlight-icon remove-btn-style"
              on:click={handleCopyKey}
              tabindex="0"
              aria-label="copy key"><Copy /></button
            >
          </div></span
        >
        <p>You can only copy this value once, save it somewhere safe.</p>
      </div>
    {/if}
  </div>
  <form method="POST" enctype="multipart/form-data" use:enhance>
    <DataTable
      bind:selectedRowIds
      headers={[
        { key: 'name', value: 'Name' },
        { key: 'api_key', value: 'Secret Keys', display: (key) => formatKey(key) },
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
        { key: 'permissions', value: 'Permissions' }
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
                row.name.toLowerCase().includes(value.toString().toLowerCase()) ||
                row.api_key.toLowerCase().includes(value.toString().toLowerCase()) ||
                formattedCreatedAtDate.includes(value.toString().toLowerCase()) ||
                formattedExpiresAtDate.includes(value.toString().toLowerCase()) ||
                row.permissions.toLowerCase().includes(value.toString().toLowerCase())
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
    <Modal
      bind:open={modalOpen}
      modalHeading="Create new API key"
      primaryButtonText="Create"
      secondaryButtonText="Cancel"
      shouldSubmitOnEnter={false}
      hasForm
      on:click:button--secondary={handleCancel}
      on:close={handleCancel}
      on:submit={() => handleSubmit()}
    >
      <div class="modal-inner-content">
        <p style="width: 70%;">
          This API key is linked to your user account and get be used to make API calls to Leapfrog
          AI. Keep this key safe and private.
        </p>

        <TextInput
          id="name"
          name="name"
          labelText="Name"
          placeholder="Test Key"
          size="sm"
          autocomplete="off"
          bind:value={$form.name}
          invalid={!!$errors.name}
          invalidText={$errors.name?.toString()}
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
  </form>

  <Modal
    danger
    bind:open={confirmDeleteModalOpen}
    modalHeading={`Delete API ${keyNames.length > 0 ? 'Keys' : 'Key'}`}
    primaryButtonText="Delete"
    secondaryButtonText="Cancel"
    shouldSubmitOnEnter={false}
    primaryButtonDisabled={deleting}
    on:click:button--secondary={() => handleCancelConfirmDelete()}
    on:close={() => handleCancelConfirmDelete()}
    on:submit={() => handleDelete()}
  >
    <p>Are you sure you want to delete <span style="font-weight: bold">{keyNames}</span>?</p>
  </Modal>
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
    gap: layout.$spacing-06;
    align-items: center;
  }

  .key-container {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: themes.$layer-01;
    padding: layout.$spacing-03;
    gap: layout.$spacing-06;
  }

  .title {
    @include type.type-style('heading-05');
  }

  .modal-inner-content {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-06;
  }

  .deleting {
    margin-right: layout.$spacing-05;
  }
</style>
