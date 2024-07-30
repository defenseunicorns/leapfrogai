<script lang="ts">
  import {
    Button,
    ButtonGroup,
    Checkbox,
    Dropdown,
    DropdownItem,
    Fileupload,
    Heading,
    Spinner,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    TableSearch
  } from 'flowbite-svelte';
  import { yup } from 'sveltekit-superforms/adapters';
  import { superForm } from 'sveltekit-superforms';
  import { formatDate } from '$helpers/dates';
  import { filesSchema } from '$schemas/files';
  import { filesStore, toastStore } from '$stores';
  import { ACCEPTED_FILE_TYPES } from '$constants';
  import { afterNavigate, invalidate } from '$app/navigation';
  import type { Assistant } from 'openai/resources/beta/assistants';
  import { formatKeyShort } from '$helpers/apiKeyHelpers';
  import { tableStyles } from '$lib/styles/tables';
  import { filterTable } from '$lib/utils/tables';
  import { onMount } from 'svelte';
  import {
    ChevronDownOutline,
    ChevronLeftOutline,
    ChevronRightOutline,
    UploadOutline
  } from 'flowbite-svelte-icons';
  import type { FileRow } from '$lib/types/files';
  import LFFileUploadBtn from '$components/LFFileUploadBtn.svelte';

  export let data;

  $: files = [...$filesStore.files, ...$filesStore.pendingUploads] as FileRow[];

  const { divClass, innerDivClass, searchClass, classInput } = tableStyles;
  const itemsPerPage = 10;
  const showPage = 5;
  const FILTER_KEYS: Array<keyof FileRow> = ['filename', 'created_at'];
  let searchTerm = '';
  let currentPosition = 0;
  let totalPages = 0;
  let pagesToShow = [];
  let totalItems = files?.length || 0;
  let startPage;
  let endPage;

  let actionsOpen = false;
  let confirmDeleteModalOpen = false;
  let allItemsChecked = false;

  let deleting = false;

  let uploadedFiles: File[] = [];
  let nonSelectableRowIds: string[] = [];
  let affectedAssistants: Assistant[];
  let affectedAssistantsLoading = false;

  $: filteredItems = filterTable(files, FILTER_KEYS, searchTerm.toLowerCase());
  $: currentPageItems = files.slice(currentPosition, currentPosition + itemsPerPage);
  $: startRange = currentPosition + 1;
  $: endRange = Math.min(currentPosition + itemsPerPage, totalItems);
  $: editMode = false;

  $: affectedAssistants = [];
  // Form error in form action (e.g. validation failure)
  $: $errors._errors && $errors._errors.length > 0 && handleFormError();

  /****** Page Handlers ******/
  const loadNextPage = () => {
    if (currentPosition + itemsPerPage < files.length) {
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
    totalPages = Math.ceil(files.length / itemsPerPage);
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
  /****** End Page Handlers ******/

  const handleFormError = () => {
    filesStore.setAllUploadingToError();
    toastStore.addToast({
      kind: 'error',
      title: 'Import Failed',
      subtitle: `${$errors._errors?.join(', ') || 'Please try again or contact support'}`
    });
  };

  const { enhance, submit, submitting, errors } = superForm(data.form, {
    validators: yup(filesSchema),
    invalidateAll: false,
    onError() {
      // Non-handled error in form action
      handleFormError();
    },
    onResult: async ({ result }) => {
      if (result.type === 'success') {
        filesStore.updateWithUploadResults(result.data?.uploadedFiles);
      }
      filesStore.setUploading(false);
    }
  });

  const handleDelete = async () => {
    affectedAssistantsLoading = true;
    confirmDeleteModalOpen = true;
    const getAffectedAssistants = await fetch(`/api/files/delete-check/`, {
      method: 'POST',
      body: JSON.stringify({ fileIds: $filesStore.selectedFileManagementFileIds })
    });
    if (getAffectedAssistants.ok) {
      const assistants = await getAffectedAssistants.json();

      if (assistants && assistants.length > 0) {
        affectedAssistants = assistants;
      }
    }

    affectedAssistantsLoading = false;
  };

  const handleConfirmedDelete = async () => {
    const isMultipleFiles = $filesStore.selectedFileManagementFileIds.length > 1;
    deleting = true;
    const res = await fetch('/api/files/delete', {
      method: 'DELETE',
      body: JSON.stringify({ ids: $filesStore.selectedFileManagementFileIds }),
      headers: {
        'Content-Type': 'application/json'
      }
    });
    confirmDeleteModalOpen = false;
    await invalidate('lf:files');
    if (res.ok) {
      toastStore.addToast({
        kind: 'success',
        title: `${isMultipleFiles ? 'Files' : 'File'} Deleted`
      });
    } else {
      toastStore.addToast({
        kind: 'error',
        title: `Error Deleting ${isMultipleFiles ? 'Files' : 'File'}`
      });
    }
    filesStore.setSelectedFileManagementFileIds([]);
    deleting = false;
  };

  const handleUpload = async () => {
    filesStore.setUploading(true);
    filesStore.addUploadingFiles(uploadedFiles);
    nonSelectableRowIds = $filesStore.pendingUploads.map((row) =>
      row.status === 'uploading' ? row.id : ''
    );
    submit(); //upload all files
  };

  $: if (uploadedFiles.length > 0) {
    //files selected by user
    handleUpload();
  }

  afterNavigate(() => {
    // Remove files with "uploading" status from store and invalidate the route so files are re-fetched
    // when the page is loaded again
    // If we want to persist the uploading status, we will have to use event streaming/supabase realtime
    filesStore.setPendingUploads(
      $filesStore.pendingUploads.filter((file) => file.status === 'error')
    );
    invalidate('lf:files');
  });

  const closeEditMode = () => {
    editMode = false;
    filesStore.setSelectedFileManagementFileIds([]);
  };

  const handleEditItem = (id: string) => {
    const index = $filesStore.selectedFileManagementFileIds.indexOf(id);
    if (index > -1) {
      filesStore.removeSelectedFileManagementFileId(id);
    } else {
      filesStore.addSelectedFileManagementFileId(id);
    }
  };

  const checkAllItems = () => {
    if (allItemsChecked) {
      selectedRowIds = [];
    } else {
      const items = searchTerm !== '' ? filteredItems : files;
      selectedRowIds = items.map((item) => item.id);
    }
  };

  onMount(() => {
    renderPagination();
  });
</script>

<Heading tag="h3">File Management</Heading>

<div class="w-3/4 bg-gray-50 p-3 dark:bg-gray-900">
  <form method="POST" enctype="multipart/form-data" use:enhance>
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
          {#if deleting}
            <Button color="red" disabled>
              <Spinner class="me-3" size="4" color="white" />Deleting...
            </Button>
          {:else}
            <Button
              color="red"
              on:click={() => (confirmDeleteModalOpen = true)}
              disabled={deleting || selectedRowIds.length === 0}>Delete</Button
            >
          {/if}

          <Button color="alternative" on:click={() => closeEditMode()}>Cancel</Button>
        {:else}
          {#if $submitting}
            <Button disabled>
              <Spinner class="me-3" size="4" color="white" />Uploading...
            </Button>
          {:else}
            <LFFileUploadBtn
              name="files"
              bind:files={uploadedFiles}
              multiple
              accept={ACCEPTED_FILE_TYPES}
            >
              Upload <UploadOutline class="ml-2" />
            </LFFileUploadBtn>
          {/if}

          <Button color="alternative">Actions<ChevronDownOutline class="ml-2 h-3 w-3 " /></Button>
          <Dropdown bind:open={actionsOpen} class="w-44 divide-y divide-gray-100">
            <DropdownItem on:click={() => (editMode = true)}>Edit</DropdownItem>
          </Dropdown>
        {/if}
      </div>
      <TableHead>
        {#if editMode}
          <TableHeadCell class="!p-4">
            <Checkbox
              data-testid="select-all-rows-checkbox"
              on:click={checkAllItems}
              bind:checked={allItemsChecked}
              aria-label="select all rows"
            />
          </TableHeadCell>
        {/if}
        <TableHeadCell padding="px-4 py-3" scope="col">Name</TableHeadCell>
        <TableHeadCell padding="px-4 py-3" scope="col">Date Added</TableHeadCell>
      </TableHead>
      <TableBody>
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
            <TableBodyCell tdClass="px-4 py-3">{item.filename}</TableBodyCell>
            <TableBodyCell tdClass="px-4 py-3"
              >{formatDate(new Date(item.created_at))}</TableBodyCell
            >
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
  </form>
</div>

<!--<div class="file-management-container">-->
<!--  <div class="title">File Management</div>-->
<!--  <form method="POST" enctype="multipart/form-data" use:enhance>-->
<!--    <DataTable-->
<!--      batchSelection={true}-->
<!--      bind:selectedRowIds={$filesStore.selectedFileManagementFileIds}-->
<!--      bind:nonSelectableRowIds-->
<!--      headers={[-->
<!--        { key: 'filename', value: 'Name', width: '75%' },-->
<!--        {-->
<!--          key: 'created_at',-->
<!--          value: 'Date Added'-->
<!--        }-->
<!--      ]}-->
<!--      rows={[...$filesStore.files, ...$filesStore.pendingUploads]}-->
<!--      sortable-->
<!--    >-->
<!--      <Toolbar>-->
<!--        <ToolbarBatchActions-->
<!--          bind:active-->
<!--          on:cancel={(e) => {-->
<!--            e.preventDefault();-->
<!--            active = false;-->
<!--            filesStore.setSelectedFileManagementFileIds([]);-->
<!--          }}-->
<!--        >-->
<!--          {#if deleting}-->
<!--            <div class="deleting">-->
<!--              <Loading withOverlay={false} small data-testid="delete-pending" />-->
<!--            </div>-->
<!--          {:else}-->
<!--            <Button-->
<!--              icon={TrashCan}-->
<!--              on:click={handleDelete}-->
<!--              disabled={$filesStore.selectedFileManagementFileIds.length === 0}>Delete</Button-->
<!--            >-->
<!--          {/if}-->
<!--        </ToolbarBatchActions>-->
<!--        <ToolbarContent>-->
<!--          <ToolbarSearch-->
<!--            bind:filteredRowIds-->
<!--            shouldFilterRows={(row, value) => {-->
<!--              // filter for filename and date-->
<!--              const formattedDate = formatDate(new Date(row.created_at * 1000)).toLowerCase();-->
<!--              return (-->
<!--                formattedDate.includes(value.toString().toLowerCase()) ||-->
<!--                row.filename.toLowerCase().includes(value.toString().toLowerCase())-->
<!--              );-->
<!--            }}-->
<!--          />-->

<!--          <FileUploaderButton-->
<!--            bind:files={uploadedFiles}-->
<!--            name="files"-->
<!--            multiple-->
<!--            disableLabelChanges-->
<!--            disabled={$submitting}-->
<!--            labelText="Upload"-->
<!--            accept={ACCEPTED_FILE_TYPES}-->
<!--          />-->
<!--        </ToolbarContent>-->
<!--      </Toolbar>-->

<!--      <svelte:fragment slot="cell" let:row let:cell>-->
<!--        {#if cell.key === 'filename' && row.status === 'uploading'}-->
<!--          <div class="item-with-status uploading">-->
<!--            <Loading data-testid="uploading-file-icon" withOverlay={false} small />-->
<!--            {cell.value}-->
<!--          </div>-->
<!--        {:else if cell.key === 'filename' && row.status === 'complete'}-->
<!--          <div class="item-with-status">-->
<!--            <CheckmarkFilled data-testid="file-uploaded-icon" color="#24a148" />-->

<!--            {cell.value}-->
<!--          </div>-->
<!--        {:else if cell.key === 'filename' && row.status === 'error'}-->
<!--          <div class="item-with-status error">-->
<!--            <ErrorFilled data-testid="file-uploaded-error-icon" color="#DA1E28" />-->
<!--            {cell.value}-->
<!--          </div>-->
<!--        {:else if cell.key === 'created_at'}-->
<!--          {cell.value ? formatDate(new Date(cell.value * 1000)) : ''}-->
<!--        {:else}-->
<!--          {cell.value}-->
<!--        {/if}-->
<!--      </svelte:fragment>-->
<!--    </DataTable>-->
<!--  </form>-->
<!--  <ConfirmAssistantDeleteModal-->
<!--    bind:open={confirmDeleteModalOpen}-->
<!--    bind:affectedAssistantsLoading-->
<!--    bind:deleting-->
<!--    bind:confirmDeleteModalOpen-->
<!--    {handleConfirmedDelete}-->
<!--    {affectedAssistants}-->
<!--  />-->
<!--</div>-->

<!--<style lang="scss">-->
<!--  .file-management-container {-->
<!--    display: flex;-->
<!--    flex-direction: column;-->
<!--    gap: 1rem;-->
<!--    padding: 0 12rem 0 12rem;-->
<!--  }-->
<!--  .title {-->
<!--    font-size: 2rem;-->
<!--    line-height: 2.5rem;-->
<!--    font-weight: 400;-->
<!--    letter-spacing: 0px;-->
<!--  }-->

<!--  .item-with-status {-->
<!--    display: flex;-->
<!--    gap: 0.5rem;-->
<!--  }-->

<!--  .uploading {-->
<!--    opacity: 50%;-->
<!--  }-->
<!--  .error {-->
<!--    opacity: 50%;-->
<!--  }-->
<!--  .deleting {-->
<!--    margin-right: 1rem;-->
<!--  }-->
<!--</style>-->
