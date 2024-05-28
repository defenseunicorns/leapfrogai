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
  import type { FileObject } from 'openai/resources/files';
  import { CheckmarkFilled, ErrorFilled, TrashCan } from 'carbon-icons-svelte';
  import { yup } from 'sveltekit-superforms/adapters';
  import { superForm } from 'sveltekit-superforms';
  import { formatDate } from '$helpers/dates';
  import { filesSchema } from '$schemas/files';
  import { toastStore } from '$stores';
  import type { FileRow } from '$lib/types/files';
  import { invalidate } from '$app/navigation';

  export let data;

  let uploadedFiles: File[] = [];
  let rows: Array<FileObject | FileRow>;
  let filteredRowIds: string[] = [];
  let selectedRowIds: string[] = [];
  let deleting = false;
  let active = selectedRowIds.length > 0;
  let nonSelectableRowIds: string[] = [];

  $: rows = data.files;
  $: if (selectedRowIds.length === 0) active = false;

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
    onResult({ result }) {
      if (result.type === 'success') {
        const uploadedFiles = result.data?.uploadedFiles;
        updateAllFileStatus(uploadedFiles);
        for (const uploadedFile of uploadedFiles) {
          if (uploadedFile.status === 'error') {
            toastStore.addToast({
              kind: 'error',
              title: 'Import Failed',
              subtitle: `${uploadedFile.filename} import failed.`
            });
          } else {
            toastStore.addToast({
              kind: 'success',
              title: 'Imported Successfully',
              subtitle: `${uploadedFile.filename} imported successfully.`
            });
          }
        }
      }
    }
  });

  const handleDelete = async () => {
    const isMultipleFiles = selectedRowIds.length > 1;
    deleting = true;
    const res = await fetch('/api/files/delete', {
      method: 'DELETE',
      body: JSON.stringify({ ids: selectedRowIds }),
      headers: {
        'Content-Type': 'application/json'
      }
    });
    await invalidate('/api/files');
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
    selectedRowIds = [];
    deleting = false;
  };

  const updateAllFileStatus = (newFiles: Array<FileObject | FileRow>) => {
    // Remove all uploading files
    rows = rows.filter((row) => row.status !== 'uploading');

    const newRows = [...rows];
    // insert newly uploaded files with updated status
    for (const file of newFiles) {
      const item: FileRow = {
        id: file.id,
        filename: file.filename,
        created_at: file.created_at,
        status: file.status === 'error' ? 'error' : 'complete'
      };
      newRows.unshift(item);
    }
    rows = [...newRows];

    // Wait 1.5 seconds, then remove error files and update status to hide for successful files
    new Promise((resolve) => setTimeout(resolve, 1500)).then(() => {
      const rowsWithoutErrors = rows.filter((row) => row.status !== 'error');
      rows = rowsWithoutErrors.map((row) => {
        const item: FileRow = { ...row, status: 'hide' };
        return item;
      });
    });
  };

  const handleUpload = async () => {
    // Add pending files as table rows
    for (const file of uploadedFiles) {
      const newFile: FileRow = {
        id: `${file.name}-${new Date()}`, // temp id
        filename: file.name,
        status: 'uploading',
        created_at: null
      };
      rows = [newFile, ...rows]; // re-assign array to trigger update in table
      nonSelectableRowIds = rows.map((row) => (row.status === 'uploading' ? row.id : ''));
    }
    submit(); //upload all files
  };

  $: if (uploadedFiles.length > 0) {
    //files selected by user
    handleUpload();
  }
</script>

<div class="file-management-container">
  <div class="title">File Management</div>
  <form method="POST" enctype="multipart/form-data" use:enhance>
    <DataTable
      batchSelection={true}
      bind:selectedRowIds
      bind:nonSelectableRowIds
      headers={[
        { key: 'filename', value: 'Name', width: '75%' },
        {
          key: 'created_at',
          value: 'Date Added'
        }
      ]}
      {rows}
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
            <Button icon={TrashCan} on:click={handleDelete} disabled={selectedRowIds.length === 0}
              >Delete</Button
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
            accept={['.pdf', 'txt']}
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
