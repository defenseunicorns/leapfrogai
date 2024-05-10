import type { PageServerLoad } from './$types';
import { error, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals: { supabase, getSession } }) => {
  const session = await getSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const { data: assistants, error: assistantsError } = await supabase
    .from('assistants')
    .select('*')
    .filter('metadata->>created_by', 'eq', session.user.id)
    .order('name', { ascending: true });

  if (assistantsError) {
    console.log(`error getting user assistants: ${JSON.stringify(assistantsError)} `);
    error(500, { message: 'Error loading assistants' });
  }

  return { title: 'LeapfrogAI - Assistants', assistants: assistants ?? [] };
};
