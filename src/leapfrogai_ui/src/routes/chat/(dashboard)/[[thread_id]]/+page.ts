import type { LFAssistant } from '$lib/types/assistants';

export const load = async ({ fetch }) => {
  const response = await fetch('/api/assistants');
  const assistants = (await response.json()) as LFAssistant[];

  return { title: 'LeapfrogAI - Assistants', assistants: assistants ?? [] };
};
