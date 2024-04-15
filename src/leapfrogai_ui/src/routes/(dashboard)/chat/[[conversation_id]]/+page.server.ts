import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from '../../../../../.svelte-kit/types/src/routes';
export const load: PageServerLoad = async ({ locals: { supabase, getSession } }) => {
	const session = await getSession();

	if (!session) {
		throw redirect(303, '/');
	}

	const { data: profile, error: profileError } = await supabase
		.from('profiles')
		.select(`username, full_name, website, avatar_url`)
		.eq('id', session.user.id)
		.single();

	const { data: conversations, error: conversationsError } = await supabase
		.from('conversations')
		.select(
			`id, label, user_id, inserted_at, messages (id, role, user_id, conversation_id, content, inserted_at)`
		)
		.eq('user_id', session.user.id)
		.returns<Conversation[]>();

	if (profileError) {
		console.log(`error getting user profile: ${JSON.stringify(profileError)}`);
		await supabase.auth.signOut();
	}
	if (conversationsError) {
		console.log(`error getting user conversations: ${JSON.stringify(conversationsError)}`);
		error(500, { message: 'Error loading conversations' });
	}

	return { title: 'LeapfrogAI - Chat', session, profile, conversations: conversations ?? [] };
};
