<script lang="ts">
  import { v4 as uuidv4 } from 'uuid';
  import { ACCEPTED_FILE_TYPES } from '$constants';
  import { ToolbarButton } from 'flowbite-svelte';
  import { PaperClipOutline } from 'flowbite-svelte-icons';
  import LFFileUploadBtn from '$components/LFFileUploadBtn.svelte';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { filesSchema } from '$schemas/files';
  import { toastStore } from '$stores';
  import { ERROR_PROCESSING_FILE_MSG_TOAST } from '$constants/toastMessages';

  export let form;
  export let uploadingFiles;
  export let attachedFileMetadata;
  export let extractedFilesText;

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
      attachedFileMetadata = attachedFileMetadata.map((file) => ({ ...file, status: 'complete' }));
      if (result.type === 'success') {
        extractedFilesText = [...extractedFilesText, ...result.data.extractedFilesText];
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
      uploadingFiles = true;

      // Metadata is limited to 512 characters, we use a short id to save space
      for (let i = 0; i < e.detail.length; i++) {
        attachedFileMetadata = [
          ...attachedFileMetadata,
          { id: i, name: e.detail[i].name, type: e.detail[i].type, status: 'uploading' }
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
