import { derived, writable } from 'svelte/store';
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
    addSelectedFileManagementFileId: (id: string) => {
      update((old) => ({
        ...old,
        selectedFileManagementFileIds: [...old.selectedFileManagementFileIds, id]
      }));
    },
    removeSelectedFileManagementFileId: (id: string) => {
      update((old) => {
        const copy = [...old.selectedFileManagementFileIds];
        const index = copy.indexOf(id);
        if (index > -1) {
          copy.splice(index, 1);
        }
        return {
          ...old,
          selectedFileManagementFileIds: [...copy]
        };
      });
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
    updateWithUploadErrors: (newFiles: Array<FileObject | FileRow>) => {
      update((old) => {
        const failedRows: FileRow[] = [];

        for (const file of newFiles) {
          if (file.status === 'error') {
            const row: FileRow = {
              id: file.id,
              filename: file.filename,
              created_at: file.created_at,
              status: 'error'
            };

            failedRows.push(row);
            toastStore.addToast({
              kind: 'error',
              title: 'Import Failed',
              subtitle: `${file.filename} import failed.`
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
          pendingUploads: failedRows
        };
      });
    },
    updateWithUploadSuccess: (newFiles: Array<FileObject | FileRow>) => {
      update((old) => {
        const successRows = [...old.files];

        for (const file of newFiles) {
          const row: FileRow = {
            id: file.id,
            filename: file.filename,
            created_at: file.created_at,
            status: 'complete'
          };

          successRows.push(row);
          toastStore.addToast({
            kind: 'success',
            title: 'Imported Successfully',
            subtitle: `${file.filename} imported successfully.`
          });

          // Remove the error files after 1.5 seconds
          new Promise((resolve) => setTimeout(resolve, 1500)).then(() => {
            update((old) => {
              const index = old.files.findIndex((f) => f.id === file.id);
              old.files[index] = { ...old.files[index], status: 'hide' };
              return {
                ...old
              };
            });
          });
        }

        return {
          ...old,
          files: successRows
        };
      });
    },
    updateFiles: () => {
      update((old) => {
        old.files.forEach((row) => (row.status = 'hide'));
        return {
          ...old,
          pendingUploads: [...old.pendingUploads.filter((row) => row.status !== 'error')]
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

const filesStore = createFilesStore();
export default filesStore;

const allFilesAndPendingUploads = derived(filesStore, ($filesStore) => [
  ...$filesStore.files,
  ...$filesStore.pendingUploads
]);
export { allFilesAndPendingUploads };
