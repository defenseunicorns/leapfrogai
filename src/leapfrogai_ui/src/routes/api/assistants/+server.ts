import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';
import type { LFAssistant } from '$lib/types/assistants';

export const GET: RequestHandler = async ({ locals: { session } }) => {

  if (!session) {
    error(401, 'Unauthorized');
  }

  try {
    const openai = getOpenAiClient(session.access_token);
    const assistantsPage = await openai.beta.assistants.list();
    const assistants = assistantsPage.data as LFAssistant[];
    return json(assistants ?? []);
  } catch (e) {
    console.error('Error fetching assistants', e);
    return json([]);
  }
};
