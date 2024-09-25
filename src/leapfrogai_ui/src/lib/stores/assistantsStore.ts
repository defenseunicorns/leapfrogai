import { writable } from 'svelte/store';
import type { LFAssistant } from '$lib/types/assistants';
import { NO_SELECTED_ASSISTANT_ID } from '$constants';

type AssistantsStore = {
  assistants: LFAssistant[];
  selectedAssistantId?: string;
};

const defaultValues: AssistantsStore = {
  assistants: [],
  selectedAssistantId: NO_SELECTED_ASSISTANT_ID
};
const createAssistantsStore = () => {
  const { subscribe, set, update } = writable<AssistantsStore>({ ...defaultValues });

  return {
    subscribe,
    set,
    update,
    setAssistants: (newAssistants: LFAssistant[]) => {
      update((old) => ({ ...old, assistants: newAssistants }));
    },
    setSelectedAssistantId: (selectedAssistantId: string) => {
      update((old) => {
        return { ...old, selectedAssistantId };
      });
    },
    addAssistant: (newAssistant: LFAssistant) => {
      update((old) => ({ ...old, assistants: [...old.assistants, newAssistant] }));
    },
    removeAssistant: (id: string) => {
      update((old) => {
        const updatedAssistants = [...old.assistants];
        const assistantIndex = updatedAssistants.findIndex(
          (assistant) => assistant.id === id
        );
        if (assistantIndex > -1) {
          updatedAssistants.splice(assistantIndex, 1);
        }
        return { ...old, assistants: updatedAssistants };
      });
    },
    updateAssistant: (newAssistant: LFAssistant) => {
      update((old) => {
        const updatedAssistants = [...old.assistants];
        const assistantIndex = updatedAssistants.findIndex(
          (assistant) => assistant.id === newAssistant.id
        );
        if (assistantIndex > -1) {
          updatedAssistants[assistantIndex] = newAssistant;
        }
        return { ...old, assistants: updatedAssistants };
      });
    }
  };
};
const assistantsStore = createAssistantsStore();
export default assistantsStore;
