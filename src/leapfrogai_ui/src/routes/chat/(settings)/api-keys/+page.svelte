<script lang="ts">
  import { fade } from 'svelte/transition';
  import {
    Button,
    Checkbox,
    Heading,
    Pagination,
    Spinner,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    TableSearch
  } from 'flowbite-svelte';
  import { ArrowLeftOutline, ArrowRightOutline, PlusOutline } from 'flowbite-svelte-icons';
  import { formatDate } from '$helpers/dates.js';
  import { formatKeyShort } from '$helpers/apiKeyHelpers';
  import type { APIKeyRow } from '$lib/types/apiKeys';
  import { filterTable } from '$lib/utils/tables';
  import { tableStyles } from '$lib/styles/tables';
  import DeleteApiKeyModal from '$components/modals/DeleteApiKeyModal.svelte';
  import CreateApiKeyModal from '$components/modals/CreateApiKeyModal.svelte';
  import { STANDARD_FADE_DURATION } from '$constants';

  export let data;

  $: filteredItems =
    searchTerm !== ''
      ? filterTable(data.apiKeys, FILTER_KEYS, searchTerm.toLowerCase())
      : [...data.apiKeys];
  $: totalItems = filteredItems.length;
  $: startRange = currentPosition + 1;
  $: endRange = Math.min(currentPosition + itemsPerPage, totalItems);
  $: editMode = selectedRowIds.length > 0;

  const FILTER_KEYS: Array<keyof APIKeyRow> = ['name', 'api_key', 'created_at', 'expires_at'];
  const { divClass, innerDivClass, searchClass, classInput, headerClass } = tableStyles;
  const itemsPerPage = 10;
  let pageItems;
  let searchTerm = '';
  let currentPosition = 0;
  let createApiKeyModalOpen = false;
  let confirmDeleteModalOpen = false;
  let allItemsChecked = false;
  let selectedRowIds: string[] = [];
  let deleting = false;

  /****** Pagination Handlers ******/
  const next = () => {
    if (currentPosition + itemsPerPage < filteredItems.length) {
      currentPosition += itemsPerPage;
    }
  };
  const previous = () => {
    if (currentPosition - itemsPerPage >= 0) {
      currentPosition -= itemsPerPage;
    }
  };

  /****** End Pagination Handlers ******/

  /****** Sorting Handlers ******/

  let sortKey = 'created_at'; // default sort key
  let sortDirection = 1; // default sort direction (ascending)

  // Define a function to sort the items
  const sortTable = (key) => {
    // If the same key is clicked, reverse the sort direction
    if (sortKey === key) {
      sortDirection = -sortDirection;
    } else {
      sortKey = key;
      sortDirection = 1;
    }
  };

  // When search term changes, reset to first page
  $: searchTerm, (currentPosition = 0);

  // Sort page items based on the sort key and direction
  $: {
    const tempPageItems = filteredItems.slice(currentPosition, currentPosition + itemsPerPage);
    const sorted = tempPageItems.sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      if (aVal < bVal) {
        return -sortDirection;
      } else if (aVal > bVal) {
        return sortDirection;
      }
      return 0;
    });
    pageItems = [...sorted];
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
      selectedRowIds = filteredItems.map((item) => item.id);
    }
  };
</script>

<div class="w-3/4 bg-gray-50 p-3 dark:bg-gray-900">
  <Heading tag="h3" class="mb-4">API Keys</Heading>
  <TableSearch
    data-testid="api-keys-table"
    placeholder="Search"
    hoverable={true}
    bind:inputValue={searchTerm}
    {divClass}
    {innerDivClass}
    {searchClass}
    {classInput}
  >
    <div slot="header" class={headerClass}>
      <!-- Button with color="alternative" adds two pixels to btn height, border-box does not prevent this. h-[42px] prevents slight screen jump-->
      <div class="h-[42px]">
        {#if editMode}
          <div
            in:fade={{ duration: STANDARD_FADE_DURATION }}
            class="flex items-center gap-2"
            data-testid="table-actions"
          >
            {#if deleting}
              <Button color="red" disabled>
                <Spinner class="me-3" size="4" color="white" />Deleting...
              </Button>
            {:else}
              <Button color="red" on:click={() => (confirmDeleteModalOpen = true)}>Delete</Button>
            {/if}

            <Button color="alternative" on:click={handleClose}>Cancel</Button>
          </div>
        {:else}
          <div in:fade={{ duration: STANDARD_FADE_DURATION }}>
            <Button on:click={() => (createApiKeyModalOpen = true)} aria-label="create new">
              <PlusOutline class="mr-2 h-3.5 w-3.5" />Create new
            </Button>
          </div>
        {/if}
      </div>
    </div>
    <TableHead>
      <TableHeadCell class="w-0 !p-4">
        <Checkbox
          data-testid="select-all-rows-checkbox"
          on:click={checkAllItems}
          bind:checked={allItemsChecked}
          aria-label="select all rows"
        />
      </TableHeadCell>

      <TableHeadCell
        on:click={() => sortTable('name')}
        padding="px-4 py-3"
        scope="col"
        class="cursor-pointer">Name</TableHeadCell
      >
      <TableHeadCell
        on:click={() => sortTable('api_key')}
        padding="px-4 py-3"
        scope="col"
        class="cursor-pointer">Secret Keys</TableHeadCell
      >
      <TableHeadCell
        on:click={() => sortTable('created_at')}
        padding="px-4 py-3"
        scope="col"
        class="cursor-pointer">Created</TableHeadCell
      >
      <TableHeadCell
        on:click={() => sortTable('expires_at')}
        padding="px-4 py-3"
        scope="col"
        class="cursor-pointer">Expires</TableHeadCell
      >
    </TableHead>
    <TableBody>
      {#each pageItems as item (item.id)}
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
  <div class="mt-2 flex items-center justify-between gap-2">
    <div class="text-sm text-gray-700 dark:text-gray-400">
      {#if endRange === 0}
        Showing <span class="font-semibold text-gray-900 dark:text-white">0</span> Entries
      {:else}
        Showing <span class="font-semibold text-gray-900 dark:text-white"
          >{startRange}-{endRange}</span
        >
        of
        <span class="font-semibold text-gray-900 dark:text-white">{totalItems}</span>
        Entries
      {/if}
    </div>

    <Pagination table on:previous={previous} on:next={next}>
      <div slot="prev" class="flex items-center gap-2 text-white">
        <ArrowLeftOutline class="me-2 h-3.5 w-3.5" />
        Prev
      </div>
      <div slot="next" class="flex items-center gap-2 text-white">
        Next
        <ArrowRightOutline class="ms-2 h-6 w-6" />
      </div>
    </Pagination>
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
