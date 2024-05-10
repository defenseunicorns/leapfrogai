import { writable } from 'svelte/store';
import { toastStore } from '$stores';
import { error } from '@sveltejs/kit';

type AssistantsStore = {
  assistants: Assistant[];
};

const defaultValues: AssistantsStore = {
  assistants: []
};

const createAssistant = async (input: NewAssistantInput) => {
  const res = await fetch('/api/assistants/new', {
    method: 'POST',
    body: JSON.stringify(input),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (res.ok) return res.json();

  return error(500, 'Error creating assistant');
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
    createAssistant: async (assistant: NewAssistantInput) => {
      const newAssistant = await createAssistant(assistant);

      if (newAssistant) {
        update((old) => {
          return {
            ...old,
            assistants: [...old.assistants, newAssistant]
          };
        });
      }
      toastStore.addToast({
        kind: 'success',
        title: 'Assistant Created.',
        subtitle: ''
      });
    }
  };
};

export default createAssistantsStore();
