export const load = async ({ fetch, depends }) => {
  depends('lf:assistants');

  const assistantsRes = await fetch('/api/assistants');
  const assistants = await assistantsRes.json();

  return { title: 'LeapfrogAI - Assistants Management', assistants };
};
