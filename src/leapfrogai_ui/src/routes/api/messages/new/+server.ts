import { error, json } from '@sveltejs/kit';
import { supabaseMessagesInputSchema } from '../../../../schemas/chat';

export async function POST({ request, locals: { supabase, getSession } }) {
	const session = await getSession();
	if (!session) {
		error(401, 'Unauthorized');
	}

	let requestData: Omit<Message, 'user_id'>;

	// Validate request body
	try {
		requestData = await request.json();
		const isValid = await supabaseMessagesInputSchema.isValid(requestData);
		if (!isValid) error(400, 'Bad Request');
	} catch {
		error(400, 'Bad Request');
	}

	const message: Message = { ...requestData, user_id: session.user.id };

	const { error: responseError, data: createdMessage } = await supabase
		.from('messages')
		.insert(message)
		.select()
		.returns<Message[]>();

	if (responseError) {
		console.log(`error creating message,  error status: ${responseError.code}: ${responseError.message}`);
		error(500, { message: 'Internal Server Error' });
	}

	return json(createdMessage[0]);
}
