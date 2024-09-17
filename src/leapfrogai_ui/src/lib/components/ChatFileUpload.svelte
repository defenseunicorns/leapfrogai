<script lang="ts">
  import { ACCEPTED_FILE_TYPES, ADJUSTED_MAX_CHARACTERS, MAX_NUM_FILES_UPLOAD } from '$constants';
  import { PaperClipOutline } from 'flowbite-svelte-icons';
  import { v4 as uuidv4 } from 'uuid';
  import LFFileUploadBtn from '$components/LFFileUploadBtn.svelte';
  import { toastStore } from '$stores';
  import {
    ERROR_PROCESSING_FILE_MSG_TOAST,
    MAX_NUM_FILES_UPLOAD_MSG_TOAST
  } from '$constants/toastMessages';
  import type { LFFile } from '$lib/types/files';
  import { ERROR_UPLOADING_FILE_MSG, FILE_CONTEXT_TOO_LARGE_ERROR_MSG } from '$constants/errors';
  import { shortenFileName } from '$helpers/stringHelpers';

  export let uploadingFiles;
  export let attachedFileMetadata;
  export let attachedFiles: LFFile[];

  let fileUploadBtnRef: HTMLInputElement;

  const handleUploadError = (errorMsg) => {
    uploadingFiles = false;
    attachedFileMetadata = [];

    toastStore.addToast({
      ...ERROR_PROCESSING_FILE_MSG_TOAST({ subtitle: errorMsg })
    });
  };

  const convertFiles = (files: LFFile[]) => {
    uploadingFiles = true;
    try {
      const promises = [];
      const parsedFiles = [];

      for (const file of files) {
        if (file.type.startsWith('audio/')) {
          parsedFiles.push({
            id: file.id,
            name: shortenFileName(file.name),
            type: file.type,
            text: 'Audio file contents were not processed',
            status: 'complete'
          });
        } else {
          const formData = new FormData();
          formData.append('file', file);

          const promise = fetch('/api/files/parse-text', {
            method: 'POST',
            body: formData
          })
            .then(async (response) => {
              if (!response.ok) {
                return {
                  id: file.id,
                  name: shortenFileName(file.name),
                  type: file.type,
                  text: ERROR_UPLOADING_FILE_MSG,
                  status: 'error',
                  errorText: ERROR_UPLOADING_FILE_MSG
                };
              }

              const result = await response.json();
              return {
                id: file.id,
                name: shortenFileName(file.name),
                type: file.type,
                text: result.text,
                status: 'complete'
              };
            })
            .catch(() => {
              return {
                id: file.id,
                name: shortenFileName(file.name),
                type: file.type,
                text: ERROR_UPLOADING_FILE_MSG,
                status: 'error',
                errorText: ERROR_UPLOADING_FILE_MSG
              };
            });

          promises.push(promise);
        }
      }

      Promise.all(promises).then((results) => {
        parsedFiles.push(...results);
        const totalTextLength = parsedFiles.reduce(
          (acc, fileMetadata) => acc + JSON.stringify(fileMetadata).length,
          0
        );

        // If this file adds too much text (larger than allowed max), remove the text and set to error status
        if (totalTextLength > ADJUSTED_MAX_CHARACTERS) {
          let lastFile = parsedFiles[parsedFiles.length - 1];
          lastFile = {
            id: lastFile.id,
            name: shortenFileName(lastFile.name),
            type: lastFile.type,
            text: '',
            status: 'error',
            errorText: FILE_CONTEXT_TOO_LARGE_ERROR_MSG
          };
        }

        attachedFileMetadata = parsedFiles;
      });
    } catch {
      handleUploadError('Internal Error');
    }
    uploadingFiles = false;
  };
</script>


  <LFFileUploadBtn
    bind:ref={fileUploadBtnRef}
    testId="upload-file-btn"
    name="files"
    outline
    multiple
    size="sm"
    on:change={(e) => {
      if (e.detail.length > MAX_NUM_FILES_UPLOAD) {
        e.detail.pop();
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

      attachedFiles = [...e.detail];
      convertFiles(e.detail);
      fileUploadBtnRef.value = '';
    }}
    accept={ACCEPTED_FILE_TYPES}
    disabled={uploadingFiles}
    class="remove-btn-style flex  rounded-lg  p-1.5 text-gray-500 hover:bg-inherit dark:hover:bg-inherit"
  >
    <PaperClipOutline class="text-gray-300" />
    <span class="sr-only">Attach file</span>
  </LFFileUploadBtn>

