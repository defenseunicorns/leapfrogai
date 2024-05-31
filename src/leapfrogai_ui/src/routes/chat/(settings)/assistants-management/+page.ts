export const load = async ({ fetch }) => {
  const response = await fetch('/api/assistants');
  const assistants = await response.json();

  return { title: 'LeapfrogAI - Assistants', assistants: assistants ?? [] };
};
