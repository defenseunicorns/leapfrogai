<script lang="ts">
  import { Button, Checkbox, Dropdown } from 'flowbite-svelte';
  import { ChevronDownOutline } from 'flowbite-svelte-icons';
  import type { FileRow, FilesForm } from '$lib/types/files';
  import { filesStore } from '$stores';
  import FileUploadButton from '$components/FileFormUploadButton.svelte';

  export let files: Pick<FileRow, 'id' | 'text'>[] = [];
  export let accept: ReadonlyArray<string> = [];
  export let filesForm: FilesForm;
  export let placement: 'top' | 'bottom' = 'top';

  const handleClick = (id: string) => {
    if ($filesStore.selectedAssistantFileIds.includes(id)) {
      filesStore.setSelectedAssistantFileIds(
        $filesStore.selectedAssistantFileIds.filter((selectedId) => selectedId !== id)
      );
    } else {
      filesStore.setSelectedAssistantFileIds([...$filesStore.selectedAssistantFileIds, id]);
    }
  };

  let open;
</script>

<div class={$$props.class}>
  <Button data-testid="file-select-dropdown-btn">
    Choose data sources<ChevronDownOutline class="ms-2 h-6 w-8 text-white dark:text-white" />
  </Button>
  <Dropdown class="w-64 space-y-3 p-3 text-sm" bind:open {placement}>
    <div class="flex justify-center">
      <FileUploadButton
        id="file-upload"
        labelText="Upload new data source"
        {accept}
        multiple
        disableLabelChanges
        {filesForm}
        open={true}
      />
    </div>
    <div class="no-scrollbar max-h-64 overflow-y-scroll">
      {#each files as file (file.id)}
        <li>
          <Checkbox
            on:click={() => handleClick(file.id)}
            checked={$filesStore.selectedAssistantFileIds.includes(file.id)}>{file.text}</Checkbox
          >
        </li>
      {/each}
    </div>
  </Dropdown>
</div>
