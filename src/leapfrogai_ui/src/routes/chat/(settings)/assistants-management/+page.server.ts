import type { PageServerLoad } from '../../../../../.svelte-kit/types/src/routes/$types';

export const load: PageServerLoad = async () => {
  return { title: 'LeapfrogAI - Assistants' };
};
