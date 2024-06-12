import { redirect } from '@sveltejs/kit';

export const load = async ({ fetch, locals: { safeGetSession } }) => {
  const { session } = await safeGetSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const promises = [fetch('/api/assistants'), fetch('/api/files')];
  const [assistantsRes, filesRes] = await Promise.all(promises);

  const assistants = await assistantsRes.json();
  const files = await filesRes.json();

  return { assistants, files };
};
