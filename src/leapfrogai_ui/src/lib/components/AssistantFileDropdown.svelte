<script lang="ts">
  import { Button, Checkbox, Dropdown } from 'flowbite-svelte';
  import { ChevronDownOutline } from 'flowbite-svelte-icons';
  import type { FilesForm } from '$lib/types/files';
  import { filesStore, toastStore } from '$stores';
  import LFFileUploadBtn from '$components/LFFileUploadBtn.svelte';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { filesSchema } from '$schemas/files';
  import type { ActionResult } from '@sveltejs/kit';

  export let accept: ReadonlyArray<string> = [];
  export let filesForm: FilesForm;
  export let placement: 'top' | 'bottom' = 'top';

  let open;

  const handleClick = (id: string) => {
    if ($filesStore.selectedAssistantFileIds.includes(id)) {
      filesStore.setSelectedAssistantFileIds(
        $filesStore.selectedAssistantFileIds.filter((selectedId) => selectedId !== id)
      );
    } else {
      filesStore.setSelectedAssistantFileIds([...$filesStore.selectedAssistantFileIds, id]);
    }
  };

  const { enhance, submit } = superForm(filesForm, {
    validators: yup(filesSchema),
    invalidateAll: false,
    onError() {
      // Backend failure, not just a single file failure
      filesStore.setAllUploadingToError();
      toastStore.addToast({
        kind: 'error',
        title: 'Upload Failed',
        subtitle: `Please try again or contact support`
      });
    },
    onResult: async ({ result }) => handleResult(result)
  });

  const handleResult = async (result: ActionResult) => {
    if (result.type === 'success') {
      const idsToSelect: string[] = [];
      const uploadedFiles = result.data?.uploadedFiles;
      filesStore.updateWithUploadErrors(result.data?.uploadedFiles);
      for (const uploadedFile of uploadedFiles) {
        idsToSelect.push(uploadedFile.id);
      }
      filesStore.addSelectedAssistantFileIds(idsToSelect);
    }
    filesStore.setUploading(false);
  };
</script>

<div class={$$props.class}>
  <Button data-testid="file-select-dropdown-btn">
    Choose data sources<ChevronDownOutline class="ms-2 h-6 w-8 text-white dark:text-white" />
  </Button>
  <Dropdown class="w-64 space-y-3 p-3 text-sm" bind:open {placement}>
    <div class="flex justify-center">
      <form
        class="file-upload-container"
        method="POST"
        enctype="multipart/form-data"
        use:enhance
        action="/chat/file-management"
      >
        <LFFileUploadBtn
          size="md"
          name="files"
          {accept}
          multiple
          on:change={async (e) => {
            const fileList = e.detail;
            filesStore.setUploading(true);
            filesStore.addUploadingFiles(fileList, { autoSelectUploadedFiles: true });
            submit();
          }}>Upload new data source</LFFileUploadBtn
        >
      </form>
    </div>
    <div data-testid="file-select-container" class="max-h-64 overflow-y-auto">
      {#each $filesStore.files?.map( (file) => ({ id: file.id, text: file.filename }) ) as file (file.id)}
        <li>
          <Checkbox
            data-testid={`${file.id}-checkbox`}
            on:click={() => handleClick(file.id)}
            checked={$filesStore.selectedAssistantFileIds.includes(file.id)}
            class="truncate">{file.text}</Checkbox
          >
        </li>
      {/each}
    </div>
  </Dropdown>
</div>
