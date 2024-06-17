import { writable } from 'svelte/store';
import type { FileObject } from 'openai/resources/files';
import type { FileRow } from '$lib/types/files';
import { invalidate } from '$app/navigation';

type FilesStore = {
  files: FileRow[];
  selectedAssistantFileIds: string[];
  uploading: boolean;
};

const defaultValues: FilesStore = {
  files: [],
  selectedAssistantFileIds: [],
  uploading: false
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
    addSelectedAssistantFileIds: (newIds: string[]) =>
      update((old) => ({
        ...old,
        selectedAssistantFileIds: [...old.selectedAssistantFileIds, ...newIds]
      })),
    setSelectedAssistantFileIds: (newIds: string[]) => {
      update((old) => ({ ...old, selectedAssistantFileIds: newIds }));
    },
    addUploadingFiles: (files: File[]) => {
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
          selectedAssistantFileIds: [...old.selectedAssistantFileIds, ...newFileIds]
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
        }

        return { ...old, files: newRows };
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

        waitThenInvalidate();

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
