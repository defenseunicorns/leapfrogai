<script lang="ts">
  import {
    Button,
    DataTable,
    FileUploaderButton,
    Loading,
    Toolbar,
    ToolbarBatchActions,
    ToolbarContent,
    ToolbarSearch
  } from 'carbon-components-svelte';
  import { CheckmarkFilled, ErrorFilled, TrashCan } from 'carbon-icons-svelte';
  import { yup } from 'sveltekit-superforms/adapters';
  import { superForm } from 'sveltekit-superforms';
  import { formatDate } from '$helpers/dates';
  import { filesSchema } from '$schemas/files';
  import { filesStore, toastStore } from '$stores';
  import { afterNavigate, invalidate } from '$app/navigation';
  import type { Assistant } from 'openai/resources/beta/assistants';
  import ConfirmAssistantDeleteModal from '$components/ConfirmAssistantDeleteModal.svelte';
  import { ACCEPTED_FILE_TYPES } from '$constants';

  export let data;

  let uploadedFiles: File[] = [];
  let filteredRowIds: string[] = [];
  let deleting = false;
  let active = $filesStore.selectedFileManagementFileIds.length > 0;
  let nonSelectableRowIds: string[] = [];
  let confirmDeleteModalOpen = false;
  let affectedAssistants: Assistant[];
  let affectedAssistantsLoading = false;

  $: affectedAssistants = [];
  $: if ($filesStore.selectedFileManagementFileIds.length === 0) active = false;

  const { enhance, submit, submitting } = superForm(data.form, {
    validators: yup(filesSchema),
    invalidateAll: false,
    onError() {
      toastStore.addToast({
        kind: 'error',
        title: 'Import Failed',
        subtitle: `Please try again or contact support`
      });
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
        title: `${isMultipleFiles ? 'Files' : 'File'} Deleted`,
        subtitle: ''
      });
    } else {
      toastStore.addToast({
        kind: 'error',
        title: `Error Deleting ${isMultipleFiles ? 'Files' : 'File'}`,
        subtitle: ''
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
</script>

<div class="file-management-container">
  <div class="title">File Management</div>
  <form method="POST" enctype="multipart/form-data" use:enhance>
    <DataTable
      batchSelection={true}
      bind:selectedRowIds={$filesStore.selectedFileManagementFileIds}
      bind:nonSelectableRowIds
      headers={[
        { key: 'filename', value: 'Name', width: '75%' },
        {
          key: 'created_at',
          value: 'Date Added'
        }
      ]}
      rows={[...$filesStore.files, ...$filesStore.pendingUploads]}
      sortable
    >
      <Toolbar>
        <ToolbarBatchActions
          bind:active
          on:cancel={(e) => {
            e.preventDefault();
            active = false;
            filesStore.setSelectedFileManagementFileIds([]);
          }}
        >
          {#if deleting}
            <div class="deleting">
              <Loading withOverlay={false} small data-testid="delete-pending" />
            </div>
          {:else}
            <Button
              icon={TrashCan}
              on:click={handleDelete}
              disabled={$filesStore.selectedFileManagementFileIds.length === 0}>Delete</Button
            >
          {/if}
        </ToolbarBatchActions>
        <ToolbarContent>
          <ToolbarSearch
            bind:filteredRowIds
            shouldFilterRows={(row, value) => {
              // filter for filename and date
              const formattedDate = formatDate(new Date(row.created_at * 1000)).toLowerCase();
              return (
                formattedDate.includes(value.toString().toLowerCase()) ||
                row.filename.toLowerCase().includes(value.toString().toLowerCase())
              );
            }}
          />

          <FileUploaderButton
            bind:files={uploadedFiles}
            name="files"
            multiple
            disableLabelChanges
            disabled={$submitting}
            labelText="Upload"
            accept={ACCEPTED_FILE_TYPES}
          />
        </ToolbarContent>
      </Toolbar>

      <svelte:fragment slot="cell" let:row let:cell>
        {#if cell.key === 'filename' && row.status === 'uploading'}
          <div class="item-with-status uploading">
            <Loading data-testid="uploading-file-icon" withOverlay={false} small />
            {cell.value}
          </div>
        {:else if cell.key === 'filename' && row.status === 'complete'}
          <div class="item-with-status">
            <CheckmarkFilled data-testid="file-uploaded-icon" color="#24a148" />

            {cell.value}
          </div>
        {:else if cell.key === 'filename' && row.status === 'error'}
          <div class="item-with-status error">
            <ErrorFilled data-testid="file-uploaded-error-icon" color="#DA1E28" />
            {cell.value}
          </div>
        {:else if cell.key === 'created_at'}
          {cell.value ? formatDate(new Date(cell.value * 1000)) : ''}
        {:else}
          {cell.value}
        {/if}
      </svelte:fragment>
    </DataTable>
  </form>
  <ConfirmAssistantDeleteModal
    bind:open={confirmDeleteModalOpen}
    bind:affectedAssistantsLoading
    bind:deleting
    bind:confirmDeleteModalOpen
    {handleConfirmedDelete}
    {affectedAssistants}
  />
</div>

<style lang="scss">
  .file-management-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0 12rem 0 12rem;
  }
  .title {
    @include type.type-style('heading-05');
  }

  .item-with-status {
    display: flex;
    gap: layout.$spacing-03;
  }

  .uploading {
    opacity: 50%;
  }
  .error {
    opacity: 50%;
  }
  .deleting {
    margin-right: layout.$spacing-05;
  }
</style>
