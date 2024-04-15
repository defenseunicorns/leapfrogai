import type { Actions } from '../../../.svelte-kit/types/src/routes/$types';
import { redirect } from '@sveltejs/kit';

export const actions: Actions = {
	signout: async ({ locals: { supabase, getSession } }) => {
		const session = await getSession();
		if (session) {
			await supabase.auth.signOut();
			throw redirect(303, '/');
		}
	}
};
