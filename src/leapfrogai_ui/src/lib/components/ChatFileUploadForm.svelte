<script lang="ts">
  import { ACCEPTED_FILE_TYPES, MAX_NUM_FILES_UPLOAD } from '$constants';
  import { PaperClipOutline } from 'flowbite-svelte-icons';
  import { v4 as uuidv4 } from 'uuid';
  import LFFileUploadBtn from '$components/LFFileUploadBtn.svelte';
  import { superForm } from 'sveltekit-superforms';
  import { yup } from 'sveltekit-superforms/adapters';
  import { filesSchema } from '$schemas/files';
  import { toastStore } from '$stores';
  import {
    ERROR_PROCESSING_FILE_MSG_TOAST,
    MAX_NUM_FILES_UPLOAD_MSG_TOAST
  } from '$constants/toastMessages';
  import type {LFFile} from "$lib/types/files";

  export let form;
  export let uploadingFiles;
  export let attachedFileMetadata;
  export let uploadedFiles: LFFile[];

  const handleUploadError = (errorMsg) => {
    uploadingFiles = false;
    attachedFileMetadata = [];

    toastStore.addToast({
      ...ERROR_PROCESSING_FILE_MSG_TOAST({ subtitle: errorMsg })
    });
  };

  const {
    form: storeForm,
    enhance,
    submit
  } = superForm(form, {
    validators: yup(filesSchema),
    invalidateAll: false,
    onResult({ result, cancel }) {
      uploadingFiles = false;
      if (result.type === 'success') {
        attachedFileMetadata = result.data.extractedFilesText;
      } else {
        handleUploadError('Internal Error');
      }
      cancel(); // cancel the rest of the event chain and any form updates to prevent losing focus of chat input
    },
    onError(e) {
      handleUploadError(e.result.error.message);
      uploadingFiles = false;
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
      uploadingFiles = true;
      for (const file of e.detail) {
        // Metadata is limited to 512 characters, we use a short id to save space
        const id = uuidv4().substring(0, 8);
        file.id = id;
        attachedFileMetadata = [
          ...attachedFileMetadata,
          {
            id,
            name: file.name,
            type: file.type,
            status: 'uploading'
          }
        ];
      }
      $storeForm.files = e.detail;
      console.log("$storeForm.files", $storeForm.files)
      uploadedFiles = [...e.detail];
      submit(e.detail);
    }}
    accept={ACCEPTED_FILE_TYPES}
    disabled={uploadingFiles}
    class="remove-btn-style flex  rounded-lg  p-1.5 text-gray-500 hover:bg-inherit dark:hover:bg-inherit"
  >
    <PaperClipOutline class="text-gray-300" />
    <span class="sr-only">Attach file</span>
  </LFFileUploadBtn>
</form>
