<script lang="ts">
  import { fade } from 'svelte/transition';
  import { writable } from 'svelte/store';
  import { formatDate } from '$helpers/dates.js';
  import type { APIKeyRow } from '$lib/types/apiKeys';
  import {
    Button,
    ButtonGroup,
    Checkbox,
    Heading,
    Spinner,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    TableSearch
  } from 'flowbite-svelte';
  import { ChevronLeftOutline, ChevronRightOutline, PlusOutline } from 'flowbite-svelte-icons';
  import { filterTable } from '$lib/utils/tables';
  import type { PageServerData } from './$types';
  import { formatKeyShort } from '$helpers/apiKeyHelpers';
  import DeleteApiKeyModal from '$components/modals/DeleteApiKeyModal.svelte';
  import { onMount } from 'svelte';
  import CreateApiKeyModal from '$components/modals/CreateApiKeyModal.svelte';

  export let data: PageServerData;

  const itemsPerPage = 10;
  const showPage = 5;
  let searchTerm = '';
  let currentPosition = 0;
  let totalPages = 0;
  let pagesToShow = [];
  let totalItems = data.keys.length;
  let startPage;
  let endPage;

  let createApiKeyModalOpen = false;
  let confirmDeleteModalOpen = false;
  let allItemsChecked = false;

  let selectedRowIds: string[] = [];
  let deleting = false;

  let divClass = 'bg-white dark:bg-gray-800 relative shadow-md sm:rounded-lg overflow-hidden';
  let innerDivClass =
    'flex flex-col md:flex-row items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4';
  let searchClass = 'w-full md:w-1/2 relative';
  let classInput =
    'text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2  pl-10';

  const FILTER_KEYS: Array<keyof APIKeyRow> = ['name', 'api_key', 'created_at', 'expires_at'];
  // TODO - data.keys not getting type inference
  $: filteredItems = filterTable(data.keys, FILTER_KEYS, searchTerm.toLowerCase());
  $: currentPageItems = data.keys.slice(currentPosition, currentPosition + itemsPerPage);
  $: startRange = currentPosition + 1;
  $: endRange = Math.min(currentPosition + itemsPerPage, totalItems);
  $: editMode = selectedRowIds.length > 0;

  /****** Pagination Handlers ******/
  const loadNextPage = () => {
    if (currentPosition + itemsPerPage < data.keys.length) {
      currentPosition += itemsPerPage;
      renderPagination();
    }
  };
  const loadPreviousPage = () => {
    if (currentPosition - itemsPerPage >= 0) {
      currentPosition -= itemsPerPage;
      renderPagination();
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
    renderPagination();
  };

  /****** End Pagination Handlers ******/

  /****** Sorting Handlers ******/

  const sortKey = writable('created_at'); // default sort key
  const sortDirection = writable(1); // default sort direction (ascending)
  const sortItems = writable([...data.keys]);

  // Define a function to sort the items
  const sortTable = (key) => {
    // If the same key is clicked, reverse the sort direction
    if ($sortKey === key) {
      sortDirection.update((val) => -val);
    } else {
      sortKey.set(key);
      sortDirection.set(1);
    }
  };

  $: {
    const key = $sortKey;
    const direction = $sortDirection;
    const items = searchTerm !== '' ? filteredItems : currentPageItems;
    const sorted = items.sort((a, b) => {
      const aVal = a[key];
      const bVal = b[key];
      if (aVal < bVal) {
        return -direction;
      } else if (aVal > bVal) {
        return direction;
      }
      return 0;
    });
    sortItems.set(sorted);
  }

  /****** End Sorting Handlers ******/

  const handleClose = () => {
    editMode = false;
    allItemsChecked = false;
    selectedRowIds = [];
  };

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

<div class="w-3/4 bg-gray-50 p-3 dark:bg-gray-900">
  <Heading tag="h3" class="mb-4">API Keys</Heading>
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
      <!-- Button with color="alternative" adds two pixels to btn height, border-box does not prevent this. h-[42px] prevents slight screen jump-->
      <div class="h-[42px]">
        {#if editMode}
          <div in:fade={{ duration: 150 }}>
            {#if deleting}
              <Button color="red" disabled>
                <Spinner class="me-3" size="4" color="white" />Deleting...
              </Button>
            {:else}
              <Button color="red" on:click={() => (confirmDeleteModalOpen = true)}>Delete</Button>
            {/if}

            <Button color="alternative" on:click={() => handleClose()}>Cancel</Button>
          </div>
        {:else}
          <div in:fade={{ duration: 150 }}>
            <Button on:click={() => (createApiKeyModalOpen = true)} aria-label="create new">
              <PlusOutline class="mr-2 h-3.5 w-3.5" />Create new
            </Button>
          </div>
        {/if}
      </div>
    </div>
    <TableHead>
      <TableHeadCell class="!p-4">
        <Checkbox
          data-testid="select-all-rows-checkbox"
          on:click={checkAllItems}
          bind:checked={allItemsChecked}
          aria-label="select all rows"
        />
      </TableHeadCell>

      <TableHeadCell on:click={() => sortTable('name')} padding="px-4 py-3" scope="col"
        >Name</TableHeadCell
      >
      <TableHeadCell on:click={() => sortTable('api_key')} padding="px-4 py-3" scope="col"
        >Secret Keys</TableHeadCell
      >
      <TableHeadCell on:click={() => sortTable('created_at')} padding="px-4 py-3" scope="col"
        >Created</TableHeadCell
      >
      <TableHeadCell on:click={() => sortTable('expires_at')} padding="px-4 py-3" scope="col"
        >Expires</TableHeadCell
      >
    </TableHead>
    <TableBody>
      {#each $sortItems as item (item.id)}
        <TableBodyRow>
          <TableHeadCell class="!p-4">
            <Checkbox
              on:click={() => handleEditItem(item.id)}
              checked={selectedRowIds.includes(item.id)}
            />
          </TableHeadCell>

          <TableBodyCell tdClass="px-4 py-3">{item.name}</TableBodyCell>
          <TableBodyCell tdClass="px-4 py-3">{formatKeyShort(item.api_key)}</TableBodyCell>
          <TableBodyCell tdClass="px-4 py-3">{formatDate(new Date(item.created_at))}</TableBodyCell>
          <TableBodyCell tdClass="px-4 py-3">{formatDate(new Date(item.expires_at))}</TableBodyCell>
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
    handleClose();
  }}
/>

<CreateApiKeyModal form={data.form} bind:createApiKeyModalOpen />
