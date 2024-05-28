import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import type { LFAssistant } from '$lib/types/assistants';
import { openai } from '$lib/server/constants';

export const load: PageServerLoad = async ({ locals: { getSession } }) => {
  const session = await getSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const assistantsPage = await openai.beta.assistants.list();

  const assistants = assistantsPage.data as LFAssistant[];

  return { title: 'LeapfrogAI - Assistants', assistants: assistants ?? [] };
};
