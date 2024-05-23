<script lang="ts">
  import {
    DataTable,
    FileUploaderButton,
    Loading,
    Toolbar,
    ToolbarContent,
    ToolbarSearch
  } from 'carbon-components-svelte';

  import { formatDate } from '$helpers/dates';
  import type { FileObject } from 'openai/src/resources/files';
  import { CheckmarkFilled, ErrorFilled } from 'carbon-icons-svelte';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { filesSchema } from '$schemas/files';
  import { toastStore } from '$stores';
  import type { FileRow } from '$lib/types/files';

  export let data;

  let uploadedFiles: File[] = [];
  let rows: Array<FileObject | FileRow>;
  $: rows = data.files;

  let filteredRowIds: string[] = [];

  const { form, enhance, submit, submitting } = superForm(data.form, {
    validators: yup(filesSchema),
    invalidateAll: false,
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

  const updateAllFileStatus = (newFiles: Array<FileObject | { name: string; error: 'true' }>) => {
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
      const newFile = {
        id: `${file.name}-${new Date()}`, // temp id
        filename: file.name,
        status: 'uploading'
      };
      rows = [newFile, ...rows]; // re-assign array to trigger update in table
    }
    submit(); //upload all files
  };

  $: if (uploadedFiles.length > 0) {
    //files selected by user
    handleUpload();
  }
</script>

<div class="file-management-container">
  <form method="POST" enctype="multipart/form-data" use:enhance>
    <div class="title">File Management</div>
    <DataTable
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
            <Loading withOverlay={false} small />
            {cell.value}
          </div>
        {:else if cell.key === 'filename' && row.status === 'complete'}
          <div class="item-with-status">
            <CheckmarkFilled color="#24a148" />

            {cell.value}
          </div>
        {:else if cell.key === 'filename' && row.status === 'error'}
          <div class="item-with-status error">
            <ErrorFilled color="#DA1E28" />
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
</style>
