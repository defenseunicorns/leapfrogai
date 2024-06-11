import { writable } from 'svelte/store';
import type { FileObject } from 'openai/resources/files';
import type { FileRow, FileUploadStatus } from '$lib/types/files';

type FilesStore = {
  files: FileObject[];
  pendingFiles: FileRow[];
  errorFiles: FileRow[];
  selectedAssistantFileIds: string[];
};

const defaultValues: FilesStore = {
  files: [],
  pendingFiles: [],
  errorFiles: [],
  selectedAssistantFileIds: []
};

const createFilesStore = () => {
  const { subscribe, set, update } = writable<FilesStore>({ ...defaultValues });

  return {
    subscribe,
    set,
    update,
    setFiles: (newFiles: FileObject[]) => {
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
    setPendingFiles: (pendingFiles: FileRow[]) => {
      update((old) => ({ ...old, pendingFiles: [...pendingFiles] }));
    },
    addErrorFile: (errorFile: FileRow) => {
      update((old) => ({ ...old, errorFiles: [...old.errorFiles, errorFile] }));
    },
    addPendingFile: async (pendingFile: FileRow) => {
      update((old) => ({ ...old, pendingFiles: [...old.pendingFiles, pendingFile] }));
    },
    updatePendingFile: (oldId: string, newId: string, status: FileUploadStatus) => {
      update((old) => {
        const index = old.pendingFiles.findIndex((file) => file.id === oldId);
        if (status === 'completed') {
          return {
            ...old,
            pendingFiles: [old.pendingFiles.slice(index, 1)],
            selectedAssistantFileIds: [...old.selectedAssistantFileIds, newId]
          }; // remove from pending
        }
        if (status === 'error') {
          const pendingFilesCopy = [...old.pendingFiles];
          pendingFilesCopy[index] = { ...pendingFilesCopy[index], status };
          return { ...old, pendingFiles: pendingFilesCopy };
        }
      });
    },
    removePendingFile: (id: string) => {
      update((old) => {
        const index = old.pendingFiles.findIndex((file) => file.id === id);
        return { ...old, pendingFiles: [old.pendingFiles.slice(index, 1)] };
      });
    }
  };
};

export default createFilesStore();
