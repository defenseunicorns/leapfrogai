import { error, json, redirect } from '@sveltejs/kit';
import { newConversationSchema } from '../../../../schemas/chat';

export async function POST({ request, locals: { supabase, getSession } }) {
	let requestData: { label: string };
	// Validate request body
	try {
		requestData = await request.json();
		const isValid = await newConversationSchema.isValid(requestData);
		if (!isValid) error(400, 'Bad Request');
	} catch {
		error(400, 'Bad Request');
	}

	const session = await getSession();

	if (!session) {
		throw redirect(303, '/');
	}

	const conversation: Omit<Conversation, 'id' | 'inserted_at' | 'messages'> = {
		label: requestData.label,
		user_id: session.user.id
	};

	// TODO validate input
	// TODO if there is an error, the chats continue to stream, but they are not saved
	// Can we trigger another call on error that retries the save?
	// At least send user a toast to let them know it was not saved (same for new message endpoint)

	const { error: responseError, data: createdConversation } = await supabase
		.from('conversations')
		.insert(conversation)
		.select()
		.returns<Conversation[]>();

	if (responseError) {
		console.log(
			`error creating conversation,  error: ${responseError.code}: ${responseError.message}`
		);
		error(500, { message: 'Internal Server Error' });
	}

	return json(createdConversation[0]);
}
