import { error, json } from '@sveltejs/kit';
import { openai } from '$lib/server/constants';
import type { LFAssistant } from '$lib/types/assistants';

export async function GET({ locals: { safeGetSession } }) {
  const { session } = await safeGetSession();

  if (!session) {
    error(401, 'Unauthorized');
  }

  const assistantsPage = await openai.beta.assistants.list();

  const assistants = assistantsPage.data as LFAssistant[];

  return json(assistants ?? []);
}
