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
    updateFileVectorStatus: (fileId: string, vectorStoreId: string, status: VectorStatus) => {
      update((old) => {
        const oldFile = old[fileId];
        if (!oldFile) {
          return { ...old, [fileId]: { [vectorStoreId]: status } };
        }
        return { ...old, [fileId]: { ...oldFile, [vectorStoreId]: status } };
      });
    },
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
    removeFile: async (fileId: string, vectorStoreId: string) => {
      update((old) => {
        old[fileId][vectorStoreId] = undefined;
        return { ...old };
      });
    }
  };
};

const vectorStatusStore = createVectorStatusStore();

export default vectorStatusStore;
