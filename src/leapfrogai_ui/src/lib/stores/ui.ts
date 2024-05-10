import { writable } from 'svelte/store';

type UIStore = {
  isSideNavOpen: boolean;
};

const defaultValues: UIStore = {
  isSideNavOpen: true
};

const createUIStore = () => {
  const { subscribe, set, update } = writable<UIStore>({ ...defaultValues });

  return {
    subscribe,
    set,
    update,
    reset: () => set({ ...defaultValues }),
    setIsSideNavOpen: (isOpen: boolean) => {
      update((old) => ({ ...old, isSideNavOpen: isOpen }));
    }
  };
};

export default createUIStore();
