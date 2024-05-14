import { writable } from 'svelte/store';

type AssistantsStore = {
  assistants: Assistant[];
};

const defaultValues: AssistantsStore = {
  assistants: []
};

const createAssistantsStore = () => {
  const { subscribe, set, update } = writable<AssistantsStore>({ ...defaultValues });
  return {
    subscribe,
    set,
    update,
    setAssistants: (assistants: Assistant[]) => {
      update((old) => ({ ...old, assistants }));
    },
    getAssistants: () => {},
    addAssistant: (newAssistant: Assistant) => {
      update((old) => ({
        ...old,
        assistants: [...old.assistants, newAssistant]
      }));
    }
  };
};

export default createAssistantsStore();
