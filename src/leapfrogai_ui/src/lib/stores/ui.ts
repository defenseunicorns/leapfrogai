import { writable } from 'svelte/store';

type UIStore = {
  isSideNavOpen: boolean;
  overflowMenuOpen: boolean;
  selectedThreadOverflowMenuId: string;
};

const defaultValues: UIStore = {
  isSideNavOpen: true,
  overflowMenuOpen: false,
  selectedThreadOverflowMenuId: ''
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
    },
    setOverflowMenuOpen: (isOpen: boolean) => {
      update((old) => ({ ...old, overflowMenuOpen: isOpen }));
    },
    setSelectedThreadOverflowMenuId: (id: string) => {
      update((old) => ({ ...old, selectedThreadOverflowMenuId: id }));
    }
  };
};

export default createUIStore();
