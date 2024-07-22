import { writable } from 'svelte/store';

type UIStore = {
  openSidebar: boolean;
};

const defaultValues: UIStore = {
  openSidebar: true
};

const createUIStore = () => {
  const { subscribe, set, update } = writable<UIStore>({ ...defaultValues });

  return {
    subscribe,
    set,
    update,
    reset: () => set({ ...defaultValues }),
    setOpenSidebar: (isOpen: boolean) => {
      update((old) => ({ ...old, openSidebar: isOpen }));
    }
  };
};

export default createUIStore();
