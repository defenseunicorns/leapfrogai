import { writable } from 'svelte/store';

type UIStore = {
  openSidebar: boolean;
  isUsingOpenAI: boolean;
};

const defaultValues: UIStore = {
  openSidebar: true,
  isUsingOpenAI: false
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
    },
    setIsUsingOpenAI: (state: boolean) => {
      update((old) => ({ ...old, isUsingOpenAI: state }));
    }
  };
};

export default createUIStore();
