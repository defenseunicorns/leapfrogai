<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { formatDate } from '$helpers/dates.js';
  import { toastStore } from '$stores';
  import { newAPIKeySchema } from '$schemas/apiKey.js';
  import { invalidate } from '$app/navigation';
  import type { APIKeyRow } from '$lib/types/apiKeys';
  import {
    Button,
    ButtonGroup,
    Checkbox,
    Dropdown,
    DropdownItem,
    Heading,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    TableSearch
  } from 'flowbite-svelte';
  import {
    ChevronDownOutline,
    ChevronLeftOutline,
    ChevronRightOutline,
    PlusOutline
  } from 'flowbite-svelte-icons';
  import { filterTable } from '$lib/utils/tables';
  import type { PageServerData } from './$types';
  import { formatKeyShort } from '$helpers/apiKeyHelpers';
  import DeleteApiKeyModal from '$components/modals/DeleteApiKeyModal.svelte';
  import { onMount } from 'svelte';

  export let data: PageServerData;

  let searchTerm = '';
  let currentPosition = 0;
  const itemsPerPage = 10;
  const showPage = 5;
  let totalPages = 0;
  let pagesToShow = [];
  let totalItems = data.keys.length;
  let startPage;
  let endPage;

  let actionsOpen = false;
  let modalOpen = false;
  let confirmDeleteModalOpen = false;
  let copyKeyModalOpen = false;
  let allItemsChecked = false;

  let selectedRowIds: string[] = [];
  let deleting = false;
  let selectedExpirationIndex = 1;
  let selectedExpirationDate: number;
  let createdKey: APIKeyRow | null = null;

  let divClass = 'bg-white dark:bg-gray-800 relative shadow-md sm:rounded-lg overflow-hidden';
  let innerDivClass =
    'flex flex-col md:flex-row items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4';
  let searchClass = 'w-full md:w-1/2 relative';
  let classInput =
    'text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2  pl-10';

  const FILTER_KEYS: Array<keyof APIKeyRow> = [
    'name',
    'api_key',
    'created_at',
    'expires_at',
    'permissions'
  ];
  // TODO - data.keys not getting type inference
  $: filteredItems = filterTable(data.keys, FILTER_KEYS, searchTerm);
  $: currentPageItems = data.keys.slice(currentPosition, currentPosition + itemsPerPage);
  $: startRange = currentPosition + 1;
  $: endRange = Math.min(currentPosition + itemsPerPage, totalItems);
  $: editMode = false;

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

  const closeEditMode = () => {
    editMode = false;
    selectedRowIds = [];
  };

  const handleCloseCopyKeyModal = () => {
    copyKeyModalOpen = false;
    createdKey = null;
  };

  /****** Page Handlers ******/

  const updateDataAndPagination = () => {
    const currentPageItems = data.keys.slice(currentPosition, currentPosition + itemsPerPage);
    renderPagination(currentPageItems.length);
  };

  const loadNextPage = () => {
    if (currentPosition + itemsPerPage < data.keys.length) {
      currentPosition += itemsPerPage;
      updateDataAndPagination();
    }
  };
  const loadPreviousPage = () => {
    if (currentPosition - itemsPerPage >= 0) {
      currentPosition -= itemsPerPage;
      updateDataAndPagination();
    }
  };

  const renderPagination = () => {
    totalPages = Math.ceil(data.keys.length / itemsPerPage);
    const currentPage = Math.ceil((currentPosition + 1) / itemsPerPage);

    startPage = currentPage - Math.floor(showPage / 2);
    startPage = Math.max(1, startPage);
    endPage = Math.min(startPage + showPage - 1, totalPages);

    pagesToShow = Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
  };

  const goToPage = (pageNumber) => {
    currentPosition = (pageNumber - 1) * itemsPerPage;
    updateDataAndPagination();
  };

  /****** End Page Handlers ******/

  const handleEditItem = (id: string) => {
    const index = selectedRowIds.indexOf(id);
    if (index > -1) {
      selectedRowIds = selectedRowIds.toSpliced(index, 1);
    } else {
      selectedRowIds = [...selectedRowIds, id];
    }
  };

  const checkAllItems = () => {
    if (allItemsChecked) {
      selectedRowIds = [];
    } else {
      const items = searchTerm !== '' ? filteredItems : data.keys;
      selectedRowIds = items.map((item) => item.id);
    }
  };

  onMount(() => {
    renderPagination();
  });
</script>

<Heading tag="h3">API Keys</Heading>

<div id="api-keys-table" class="bg-gray-50 p-3 dark:bg-gray-900 sm:p-5">
  <TableSearch
    placeholder="Search"
    hoverable={true}
    bind:inputValue={searchTerm}
    {divClass}
    {innerDivClass}
    {searchClass}
    {classInput}
  >
    <div
      slot="header"
      class="flex w-full flex-shrink-0 flex-col items-stretch justify-end space-y-2 md:w-auto md:flex-row md:items-center md:space-x-3 md:space-y-0"
    >
      {#if editMode}
        <Button
          color="red"
          on:click={() => (confirmDeleteModalOpen = true)}
          disabled={deleting || selectedRowIds.length === 0}>Delete</Button
        >
        <Button color="alternative" on:click={() => closeEditMode()}>Cancel</Button>
      {:else}
        <Button>
          <PlusOutline class="mr-2 h-3.5 w-3.5" />Create new
        </Button>
        <Button color="alternative">Actions<ChevronDownOutline class="ml-2 h-3 w-3 " /></Button>
        <Dropdown bind:open={actionsOpen} class="w-44 divide-y divide-gray-100">
          <DropdownItem on:click={() => (editMode = true)}>Edit</DropdownItem>
        </Dropdown>
      {/if}
    </div>
    <TableHead>
      {#if editMode}
        <TableHeadCell class="!p-4">
          <Checkbox on:click={checkAllItems} bind:checked={allItemsChecked} />
        </TableHeadCell>
      {/if}
      <TableHeadCell padding="px-4 py-3" scope="col">Name</TableHeadCell>
      <TableHeadCell padding="px-4 py-3" scope="col">Secret Keys</TableHeadCell>
      <TableHeadCell padding="px-4 py-3" scope="col">Created</TableHeadCell>
      <TableHeadCell padding="px-4 py-3" scope="col">Expires</TableHeadCell>
      <TableHeadCell padding="px-4 py-3" scope="col">Permissions</TableHeadCell>
    </TableHead>
    <TableBody class="divide-y">
      {#each searchTerm !== '' ? filteredItems : currentPageItems as item (item.id)}
        <TableBodyRow>
          {#if editMode}
            <TableHeadCell class="!p-4">
              <Checkbox
                on:click={() => handleEditItem(item.id)}
                checked={selectedRowIds.includes(item.id)}
              />
            </TableHeadCell>
          {/if}
          <TableBodyCell tdClass="px-4 py-3">{item.name}</TableBodyCell>
          <TableBodyCell tdClass="px-4 py-3">{formatKeyShort(item.api_key)}</TableBodyCell>
          <TableBodyCell tdClass="px-4 py-3">{formatDate(new Date(item.created_at))}</TableBodyCell>
          <TableBodyCell tdClass="px-4 py-3">{formatDate(new Date(item.expires_at))}</TableBodyCell>
          <TableBodyCell tdClass="px-4 py-3">{item.permissions?.join(', ') || ''}</TableBodyCell>
        </TableBodyRow>
      {/each}
    </TableBody>
  </TableSearch>
  <div
    class="flex flex-col items-start justify-between space-y-3 p-4 md:flex-row md:items-center md:space-y-0"
    aria-label="Table navigation"
  >
    <span class="text-sm font-normal text-gray-500 dark:text-gray-400">
      Showing
      <span class="font-semibold text-gray-900 dark:text-white">{startRange}-{endRange}</span>
      of
      <span class="font-semibold text-gray-900 dark:text-white">{totalItems}</span>
    </span>
    <ButtonGroup>
      <Button on:click={loadPreviousPage} disabled={currentPosition === 0}
        ><ChevronLeftOutline size="xs" class="m-1.5" /></Button
      >
      {#each pagesToShow as pageNumber}
        <Button on:click={() => goToPage(pageNumber)}>{pageNumber}</Button>
      {/each}
      <Button on:click={loadNextPage} disabled={totalPages === endPage}
        ><ChevronRightOutline size="xs" class="m-1.5" /></Button
      >
    </ButtonGroup>
  </div>
</div>

<DeleteApiKeyModal
  bind:confirmDeleteModalOpen
  {selectedRowIds}
  bind:deleting
  on:delete={() => {
    confirmDeleteModalOpen = false;
    selectedRowIds = [];
    editMode = false;
  }}
/>
