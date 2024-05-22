<script lang="ts">
  import {
    Button,
    DataTable,
    Toolbar,
    ToolbarContent,
    ToolbarSearch
  } from 'carbon-components-svelte';
  import { Upload } from 'carbon-icons-svelte';
  import { formatDate } from '$helpers/dates';

  export let data;

  $: rows = data.files;

  let filteredRowIds: string[] = [];
</script>

<div class="file-management-container">
  <div class="title">File Management</div>
  <DataTable
    headers={[
      { key: 'filename', value: 'Name', width: '75%' },
      {
        key: 'created_at',
        value: 'Date Added',
        display: (unixSeconds) => formatDate(new Date(unixSeconds * 1000))
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
        <Button icon={Upload}>Upload</Button>
      </ToolbarContent>
    </Toolbar>
  </DataTable>
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
</style>
