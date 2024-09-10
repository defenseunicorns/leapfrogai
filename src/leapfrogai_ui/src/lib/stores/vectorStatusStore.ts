/*
  This store keeps track of files and any vector stores they are in along with their processing status.
  The statuses are updating via a Supabase realtime listener.
 */

import { writable } from 'svelte/store';
import type { VectorStatus } from '$lib/types/files';
import { toastStore } from '$stores/index';

type FileVectorStatuses = {
  [fileId: string]: {
    [vectorStoreId: string]: VectorStatus;
  };
};

const createVectorStatusStore = () => {
  const { subscribe, set, update } = writable<FileVectorStatuses>({});

  return {
    subscribe,
    set,
    update,
    // Update single file's vector status
    updateFileVectorStatus: (fileId: string, vectorStoreId: string, status: VectorStatus) => {
      update((old) => {
        const oldFile = old[fileId];
        if (!oldFile) {
          return { ...old, [fileId]: { [vectorStoreId]: status } };
        }
        return { ...old, [fileId]: { ...oldFile, [vectorStoreId]: status } };
      });
    },
    // Fetch all files in the vector store and update their status
    updateAllStatusesForVector: async (vectorStoreId: string) => {
      const res = await fetch(`/api/vector-stores/files?id=${vectorStoreId}`);
      if (res.ok) {
        const data = await res.json();
        update((old) => {
          for (const file of data.body.data) {
            old[file.id] = { [vectorStoreId]: file.status };
          }
          return { ...old };
        });
      } else {
        toastStore.addToast({ kind: 'error', title: 'Error getting file vector statuses' });
      }
    },
    removeVectorStoreStatusFromFile: (fileId: string, vectorStoreId: string) => {
      update((old) => {
        if (old[fileId]) {
          delete old[fileId][vectorStoreId];
          if (Object.keys(old[fileId]).length === 0) {
            delete old[fileId];
          }
        }
        return { ...old };
      });
    },
    removeFiles: (fileIds: string[]) => {
      update((old) => {
        for (const id of fileIds) {
          delete old[id];
        }
        return { ...old };
      });
    }
  };
};

const vectorStatusStore = createVectorStatusStore();

export default vectorStatusStore;
