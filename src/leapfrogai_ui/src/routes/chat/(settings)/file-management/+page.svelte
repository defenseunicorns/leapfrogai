<script lang="ts">
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
  import { fade } from 'svelte/transition';
  import { yup } from 'sveltekit-superforms/adapters';
  import { superForm } from 'sveltekit-superforms';
  import { convertToMilliseconds, formatDate } from '$helpers/dates';
  import { filesSchema } from '$schemas/files';
  import { filesStore, toastStore, uiStore } from '$stores';
  import { ACCEPTED_DOC_TYPES, STANDARD_FADE_DURATION } from '$constants';
  import { beforeNavigate } from '$app/navigation';
  import type { Assistant } from 'openai/resources/beta/assistants';
  import { tableStyles } from '$lib/styles/tables';
  import { filterTable } from '$lib/utils/tables';
  import {
    ArrowLeftOutline,
    ArrowRightOutline,
    CheckOutline,
    CloseCircleOutline,
    UploadOutline
  } from 'flowbite-svelte-icons';
  import type { LFFileObject } from '$lib/types/files';
  import LFFileUploadBtn from '$components/LFFileUploadBtn.svelte';
  import ConfirmFilesDeleteModal from '$components/modals/ConfirmFilesDeleteModal.svelte';
  import { allFilesAndPendingUploads } from '$stores/filesStore';
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';

  export let data;

  $: filteredItems =
    searchTerm !== ''
      ? filterTable($allFilesAndPendingUploads, FILTER_KEYS, searchTerm.toLowerCase())
      : $allFilesAndPendingUploads;
  $: totalItems = filteredItems.length;
  $: startRange = currentPosition + 1;
  $: endRange = Math.min(currentPosition + itemsPerPage, totalItems);
  $: editMode = $filesStore.selectedFileManagementFileIds.length > 0;
  $: affectedAssistants = [];
  // Form error in form action (e.g. validation failure)
  $: $errors._errors && $errors._errors.length > 0 && handleFormError();

  const FILTER_KEYS: Array<keyof LFFileObject> = ['filename', 'created_at'];
  const { divClass, innerDivClass, searchClass, classInput, headerClass } = tableStyles;
  const itemsPerPage = 10;
  let pageItems;
  let searchTerm = '';
  let currentPosition = 0;
  let totalItems = $allFilesAndPendingUploads?.length || 0;
  let confirmDeleteModalOpen = false;
  let allItemsChecked = false;
  let nonSelectableRowIds: string[] = [];
  let affectedAssistants: Assistant[];
  let affectedAssistantsLoading = false;
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
      filesStore.setSelectedFileManagementFileIds([]);
    } else {
      const items = searchTerm !== '' ? filteredItems : $allFilesAndPendingUploads;
      const selectableItems = items.filter((item) => !nonSelectableRowIds.includes(item.id));
      filesStore.setSelectedFileManagementFileIds(selectableItems.map((item) => item.id));
    }
  };

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
        if ($uiStore.isUsingOpenAI) {
          filesStore.updateWithUploadErrors(result.data?.uploadedFiles);
          filesStore.updateWithUploadSuccess(result.data?.uploadedFiles);
        } else {
          // File upload call has completed, check for any files that had errors and update the store
          // Successful uploads are handled by realtime listener
          filesStore.updateWithUploadErrors(result.data?.uploadedFiles);
        }
      }
      filesStore.setUploading(false);
    }
  });

  const handleDelete = async () => {
    affectedAssistantsLoading = true;
    confirmDeleteModalOpen = true;
    const getAffectedAssistants = await fetch(`/api/files/delete/check`, {
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

  const handleUpload = async (files: File[]) => {
    filesStore.setUploading(true);
    filesStore.addUploadingFiles(files);
    nonSelectableRowIds = $filesStore.pendingUploads.map((row) =>
      row.status === 'uploading' ? row.id : ''
    );
    submit(); //upload all files
  };

  const handleDownload = async () => {
    let currentFilename;
    if (browser) {
      try {
        for (const id of $filesStore.selectedFileManagementFileIds) {
          const res = await fetch(`/api/files/${id}`);
          if (!res.ok) {
            throw new Error(`Failed to fetch file with id ${id}`);
          }
          currentFilename = $filesStore.files.find((f) => f.id === id)?.filename;
          const blob = await res.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = currentFilename || `file_${id}`;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
        }
        toastStore.addToast({
          kind: 'success',
          title: `File${$filesStore.selectedFileManagementFileIds.length > 1 ? 's' : ''} Downloaded`
        });
        filesStore.setSelectedFileManagementFileIds([]); // deselect all
      } catch {
        toastStore.addToast({
          kind: 'error',
          title: 'Download Failed',
          subtitle: currentFilename && `Download of file ${currentFilename} failed.`
        });
      }
    }
  };
  onMount(() => {
    if ($filesStore.needsUpdate) {
      filesStore.fetchFiles();
    }
  });
  beforeNavigate(() => {
    // Remove files with "uploading" status from store and set needsUpdate true so files are re-fetched
    // when the page is loaded again
    // If we want to persist the uploading status, the backend will need to implement this endpoint:
    // https://platform.openai.com/docs/api-reference/uploads
    if ($filesStore.pendingUploads.length > 0) {
      filesStore.setPendingUploads(
        $filesStore.pendingUploads.filter((file) => file.status === 'error')
      );
      filesStore.setNeedsUpdate(true);
    }
  });
</script>

<div class="w-3/4 bg-gray-50 p-3 dark:bg-gray-900">
  <Heading tag="h3" class="mb-4">File Management</Heading>
  <form method="POST" enctype="multipart/form-data" use:enhance>
    <TableSearch
      data-testid="file-management-table"
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
              <Button color="blue" on:click={handleDownload}>Download</Button>
              {#if deleting}
                <Button color="red" disabled>
                  <Spinner class="me-3" size="4" color="white" />Deleting...
                </Button>
              {:else}
                <Button color="red" on:click={handleDelete}>Delete</Button>
              {/if}

              <Button color="alternative" on:click={handleClose}>Cancel</Button>
            </div>
          {:else}
            <div in:fade={{ duration: STANDARD_FADE_DURATION }}>
              {#if $submitting}
                <Button disabled>
                  <Spinner class="me-3" size="4" color="white" />Uploading...
                </Button>
              {:else}
                <LFFileUploadBtn
                  name="files"
                  multiple
                  accept={ACCEPTED_DOC_TYPES}
                  on:change={(e) => {
                    const fileList = e.detail;
                    handleUpload(fileList);
                  }}
                >
                  Upload <UploadOutline class="ml-2" />
                </LFFileUploadBtn>
              {/if}
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

        <TableHeadCell
          padding="px-4 py-3"
          scope="col"
          on:click={() => sortTable('filename')}
          class="cursor-pointer">Name</TableHeadCell
        >
        <TableHeadCell
          padding="px-4 py-3"
          scope="col"
          on:click={() => sortTable('created_at')}
          class="cursor-pointer">Date Added</TableHeadCell
        >
      </TableHead>
      <TableBody>
        {#each pageItems as item (item.id)}
          <TableBodyRow>
            <TableHeadCell class="w-0 !p-4">
              {#if item.status !== 'uploading'}
                <Checkbox
                  on:click={() => handleEditItem(item.id)}
                  checked={$filesStore.selectedFileManagementFileIds.includes(item.id)}
                  disabled={nonSelectableRowIds.includes(item.id)}
                />
              {/if}
            </TableHeadCell>
            {#if item.status === 'uploading'}
              <TableBodyCell tdClass="px-4 py-3">
                <div class="flex gap-2">
                  <Spinner data-testid="uploading-file-spinner" size={6} />
                  {item.filename}
                </div>
              </TableBodyCell>
            {:else if item.status === 'complete'}
              <TableBodyCell tdClass="px-4 py-3">
                <div class="flex gap-2">
                  <CheckOutline data-testid="file-uploaded-icon" color="green" />
                  {item.filename}
                </div>
              </TableBodyCell>
            {:else if item.status === 'error'}
              <TableBodyCell tdClass="px-4 py-3">
                <div class="flex gap-2">
                  <div class="flex gap-2">
                    <CloseCircleOutline data-testid="file-uploaded-error-icon" color="red" />
                    {item.filename}
                  </div>
                </div>
              </TableBodyCell>
            {:else}
              <TableBodyCell tdClass="px-4 py-3">{item.filename}</TableBodyCell>
            {/if}
            {#if item.created_at}
              <TableBodyCell tdClass="px-4 py-3"
                >{formatDate(new Date(convertToMilliseconds(item.created_at)))}</TableBodyCell
              >
            {/if}
          </TableBodyRow>
        {/each}
      </TableBody>
    </TableSearch>
  </form>
  <!--Note - the Pagination component must be outside of the form or it will cause a SuperForm related TypeError in
  the unit tests: Cannot read properties of undefined (reading '$set')
    -->
  <div class="mt-2 flex items-center justify-between gap-2">
    <div class="text-sm text-gray-700 dark:text-gray-400">
      {#if endRange === 0}
        Showing <span
          data-testid="pagination-range"
          class="font-semibold text-gray-900 dark:text-white">0</span
        > Entries
      {:else}
        Showing <span
          data-testid="pagination-range"
          class="font-semibold text-gray-900 dark:text-white">{startRange}-{endRange}</span
        >
        of
        <span data-testid="pagination-total" class="font-semibold text-gray-900 dark:text-white"
          >{totalItems}</span
        >
        Entries
      {/if}
    </div>
    <Pagination table on:previous={previous} on:next={next}>
      <div slot="prev" class="flex items-center gap-2 text-white" data-testid="prev-btn">
        <ArrowLeftOutline class="me-2 h-3.5 w-3.5" />
        Prev
      </div>
      <div slot="next" class="flex items-center gap-2 text-white" data-testid="next-btn">
        Next
        <ArrowRightOutline class="ms-2 h-6 w-6" />
      </div>
    </Pagination>
  </div>

  <ConfirmFilesDeleteModal
    bind:open={confirmDeleteModalOpen}
    bind:affectedAssistantsLoading
    bind:deleting
    {affectedAssistants}
    on:delete={handleClose}
  />
</div>
