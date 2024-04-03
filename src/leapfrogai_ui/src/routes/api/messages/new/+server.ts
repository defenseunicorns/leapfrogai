import { error, json, redirect } from '@sveltejs/kit';

export async function POST({ request, locals: { supabase, getSession } }) {
	const session = await getSession();

	if (!session) {
		throw redirect(303, '/');
	}
	const requestData = await request.json();

	const message: Omit<Message, 'id' | 'inserted_at'> = { ...requestData, user_id: session.user.id };

	// TODO validate message input

	const { error: responseError, data: createdMessage } = await supabase
		.from('messages')
		.insert(message)
		.select()
		.returns<Message[]>();

	if (responseError) {
		console.log(`error creating message,  error: ${responseError.code}: ${responseError.message}`);
		error(500, { message: 'Internal Server Error' });
	}

	return json(createdMessage[0]);
}
