<script lang="ts">
  import {
    Button,
    ContentSwitcher,
    DataTable,
    Modal,
    Switch,
    TextInput,
    Toolbar,
    ToolbarContent,
    ToolbarSearch
  } from 'carbon-components-svelte';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { formatDate } from '$helpers/dates';
  import { Add } from 'carbon-icons-svelte';
  import { toastStore } from '$stores';
  import { newAPIKeySchema } from '$schemas/apiKey.js';
  import { invalidate } from '$app/navigation';

  export let data;

  let selectedRowIds: string[] = [];
  let filteredRowIds: string[] = [];
  let modalOpen = false;
  let selectedExpirationIndex = 1;
  let selectedExpirationDate: number;

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

  const { form, errors, enhance, submit, reset } = superForm(data.form, {
    invalidateAll: false,
    validators: yup(newAPIKeySchema),
    onResult({ result }) {
      if (result.type === 'success') {
        modalOpen = false;
        toastStore.addToast({
          kind: 'success',
          title: 'API key created',
          subtitle: ''
        });
        invalidate('lf:api-keys');
      } else if (result.type === 'error') {
        toastStore.addToast({
          kind: 'error',
          title: `Error creating API Key`,
          subtitle: 'Please try again or contact support'
        });
      }
    }
  });

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
</script>

<div class="container">
  <div class="title">API Keys</div>
  <form method="POST" enctype="multipart/form-data" use:enhance>
    <DataTable
      bind:selectedRowIds
      headers={[
        { key: 'name', value: 'Name' },
        { key: 'key', value: 'Secret Keys', display: (key) => formatKey(key) },
        {
          key: 'created_at',
          value: 'Created',
          display: (created_at) => formatDate(new Date(created_at))
        },
        {
          key: 'expiration',
          value: 'Expires',
          display: (created_at) => formatDate(new Date(created_at))
        },
        { key: 'permissions', value: 'Permissions' }
      ]}
      rows={data.keys || []}
      sortable
    >
      <Toolbar>
        <ToolbarContent>
          <ToolbarSearch
            bind:filteredRowIds
            shouldFilterRows={(row, value) => {
              // filter for name and date
              const formattedDate = formatDate(new Date(row.created_at * 1000)).toLowerCase();
              return (
                formattedDate.includes(value.toString().toLowerCase()) ||
                row.name.toLowerCase().includes(value.toString().toLowerCase())
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
          name="name"
          labelText="Name"
          placeholder="Test Key"
          size="sm"
          autocomplete="off"
          bind:value={$form.name}
          invalid={!!$errors.name}
          invalidText={$errors.name?.toString()}
        />
        <ContentSwitcher size="xl" style="width: 60%" bind:selectedIndex={selectedExpirationIndex}>
          <Switch text="7 Days" />
          <Switch text="30 Days" />
          <Switch text="60 Days" />
          <Switch text="90 Days" />
        </ContentSwitcher>
        <input type="hidden" name="expiration" value={selectedExpirationDate} />
      </div>
    </Modal>
  </form>
</div>

<style lang="scss">
  .container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0 12rem 0 12rem;
  }

  .title {
    @include type.type-style('heading-05');
  }

  .modal-inner-content {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-06;
  }
</style>
