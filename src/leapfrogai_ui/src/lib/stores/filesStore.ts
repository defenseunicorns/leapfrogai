import { writable } from 'svelte/store';
import type { FileObject } from 'openai/resources/files';
import type { FileRow } from '$lib/types/files';
import { toastStore } from '$stores/index';

type FilesStore = {
  files: FileRow[];
  selectedFileManagementFileIds: string[];
  selectedAssistantFileIds: string[];
  uploading: boolean;
  pendingUploads: FileRow[];
};

const defaultValues: FilesStore = {
  files: [],
  selectedFileManagementFileIds: [],
  selectedAssistantFileIds: [],
  uploading: false,
  pendingUploads: []
};

const createFilesStore = () => {
  const { subscribe, set, update } = writable<FilesStore>({ ...defaultValues });

  return {
    subscribe,
    set,
    update,
    setUploading: (status: boolean) => update((old) => ({ ...old, uploading: status })),
    setFiles: (newFiles: FileRow[]) => {
      update((old) => ({ ...old, files: [...newFiles] }));
    },
    setPendingUploads: (newFiles: FileRow[]) => {
      update((old) => ({ ...old, pendingUploads: [...newFiles] }));
    },
    setSelectedFileManagementFileIds: (newIds: string[]) => {
      update((old) => ({ ...old, selectedFileManagementFileIds: newIds }));
    },
    addSelectedAssistantFileIds: (newIds: string[]) =>
      update((old) => ({
        ...old,
        selectedAssistantFileIds: [...old.selectedAssistantFileIds, ...newIds]
      })),
    setSelectedAssistantFileIds: (newIds: string[]) => {
      update((old) => ({ ...old, selectedAssistantFileIds: newIds }));
    },
    addUploadingFiles: (files: File[], { autoSelectUploadedFiles = false } = {}) => {
      update((old) => {
        const newFiles: FileRow[] = [];
        const newFileIds: string[] = [];
        for (const file of files) {
          const id = `${file.name}-${new Date()}`; // temp id
          newFiles.push({
            id,
            filename: file.name,
            status: 'uploading',
            created_at: null
          });
          newFileIds.push(id);
        }
        return {
          ...old,
          selectedAssistantFileIds: autoSelectUploadedFiles
            ? [...old.selectedAssistantFileIds, ...newFileIds]
            : old.selectedAssistantFileIds,
          pendingUploads: newFiles
        };
      });
    },
    updateWithUploadResults: (newFiles: Array<FileObject | FileRow>) => {
      update((old) => {
        const successRows = [...old.files];
        const failedRows: FileRow[] = [];

        for (const file of newFiles) {
          const row: FileRow = {
            id: file.id,
            filename: file.filename,
            created_at: file.created_at,
            status: file.status === 'error' ? 'error' : 'complete'
          };
          if (file.status === 'error') {
            failedRows.push(row);
            toastStore.addToast({
              kind: 'error',
              title: 'Import Failed',
              subtitle: `${file.filename} import failed.`
            });
          } else {
            successRows.push(row);
            toastStore.addToast({
              kind: 'success',
              title: 'Imported Successfully',
              subtitle: `${file.filename} imported successfully.`
            });
          }
        }

        // Remove the error files after 1.5 seconds
        new Promise((resolve) => setTimeout(resolve, 1500)).then(() => {
          update((old) => {
            old.files.forEach((row) => (row.status = 'hide'));
            return {
              ...old,
              pendingUploads: [...old.pendingUploads.filter((row) => row.status !== 'error')]
            };
          });
        });

        return {
          ...old,
          files: successRows,
          pendingUploads: failedRows
        };
      });
    },
    setAllUploadingToError: () => {
      update((old) => {
        const modifiedFiles = old.pendingUploads.map((file) => {
          file.status = 'error';

          return file;
        });

        // Remove the error files after 1.5 seconds
        new Promise((resolve) => setTimeout(resolve, 1500)).then(() => {
          update((old) => {
            return {
              ...old,
              pendingUploads: []
            };
          });
        });

        return {
          ...old,
          pendingUploads: modifiedFiles,
          uploading: false
        };
      });
    }
  };
};

export default createFilesStore();
