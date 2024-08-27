<script lang="ts">
  import { ACCEPTED_FILE_TYPES, MAX_NUM_FILES_UPLOAD } from '$constants';
  import { ToolbarButton } from 'flowbite-svelte';
  import { PaperClipOutline } from 'flowbite-svelte-icons';
  import LFFileUploadBtn from '$components/LFFileUploadBtn.svelte';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { filesSchema } from '$schemas/files';
  import { toastStore } from '$stores';
  import {
    ERROR_PROCESSING_FILE_MSG_TOAST,
    MAX_NUM_FILES_UPLOAD_MSG_TOAST
  } from '$constants/toastMessages';

  export let form;
  export let uploadingFiles;
  export let attachedFileMetadata;

  const handleUploadError = (errorMsg) => {
    uploadingFiles = false;
    attachedFileMetadata = [];

    toastStore.addToast({
      ...ERROR_PROCESSING_FILE_MSG_TOAST({ subtitle: errorMsg })
    });
  };

  const { enhance, submit } = superForm(form, {
    validators: yup(filesSchema),
    invalidateAll: false,
    onResult({ result }) {
      uploadingFiles = false;
      if (result.type === 'success') {
        attachedFileMetadata = attachedFileMetadata.filter((file) => file.status !== 'uploading');
        attachedFileMetadata = [...attachedFileMetadata, ...result.data.extractedFilesText];
      } else {
        handleUploadError('Internal Error');
      }
    },
    onError(e) {
      handleUploadError(e.result.error.message);
    }
  });
</script>

<form method="POST" enctype="multipart/form-data" use:enhance>
  <LFFileUploadBtn
    testId="upload-file-btn"
    name="files"
    outline
    multiple
    size="sm"
    on:change={(e) => {
      if (e.detail.length > MAX_NUM_FILES_UPLOAD) {
        toastStore.addToast(MAX_NUM_FILES_UPLOAD_MSG_TOAST());
        return;
      }
      // Metadata is limited to 512 characters, we use a short id to save space
      for (const file of e.detail) {
        attachedFileMetadata = [
          ...attachedFileMetadata,
          { name: file.name, type: file.type, status: 'uploading' }
        ];
      }

      submit(e.detail);
    }}
    accept={ACCEPTED_FILE_TYPES}
    class="remove-btn-style flex"
  >
    <ToolbarButton
      color="dark"
      class="rounded-full text-gray-500 dark:text-gray-400"
      disabled={uploadingFiles}
      on:click={(e) => e.preventDefault()}
    >
      <PaperClipOutline />
      <span class="sr-only">Attach file</span>
    </ToolbarButton>
  </LFFileUploadBtn>
</form>
