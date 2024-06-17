import { writable } from 'svelte/store';
import type { FileObject } from 'openai/resources/files';
import type { FileRow, FilesForm } from '$lib/types/files';
import { invalidate } from '$app/navigation';
import { filesStore, toastStore } from '$stores/index';
import { superForm } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { filesSchema } from '$schemas/files';

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
  uploading: false
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
          files: [...old.files, ...newFiles],
          selectedAssistantFileIds: autoSelectUploadedFiles
            ? [...old.selectedAssistantFileIds, ...newFileIds]
            : old.selectedAssistantFileIds,
          pendingUploads: newFiles
        };
      });
    },
    updateWithUploadResults: (newFiles: Array<FileObject | FileRow>) => {
      update((old) => {
        const newRows = old.files.filter((file) => file.status !== 'uploading'); // get original rows without the uploads
        // insert newly uploaded files with updated status
        for (const file of newFiles) {
          const item: FileRow = {
            id: file.id,
            filename: file.filename,
            created_at: file.created_at,
            status: file.status === 'error' ? 'error' : 'complete'
          };
          newRows.unshift(item);

          if (file.status === 'error') {
            toastStore.addToast({
              kind: 'error',
              title: 'Import Failed',
              subtitle: `${file.filename} import failed.`
            });
          } else {
            toastStore.addToast({
              kind: 'success',
              title: 'Imported Successfully',
              subtitle: `${file.filename} imported successfully.`
            });
          }
        }

        return { ...old, files: newRows };
      });
    },
    waitThenInvalidate: () => {
      new Promise((resolve) => setTimeout(resolve, 1500)).then(() => {
        invalidate('lf:files');
      });
    },
    setAllUploadingToError: () => {
      update((old) => {
        const modifiedFiles = old.files.map((file) => {
          if (file.status === 'uploading') {
            file.status = 'error';
          }
          return file;
        });

        return {
          ...old,
          files: modifiedFiles,
          uploading: false
        };
      });
    }
  };
};

export default createFilesStore();
