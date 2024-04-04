import { error } from '@sveltejs/kit';
import { updateConversationSchema } from '../../../../../schemas/chat';

export async function PUT({ request, locals: { supabase, getSession } }) {
	const session = await getSession();
	if (!session) {
		error(401, 'Unauthorized');
	}

	let requestData: { id: string; label: string };
	// Validate request body
	try {
		requestData = await request.json();
		const isValid = await updateConversationSchema.isValid(requestData);
		if (!isValid) error(400, 'Bad Request');
	} catch {
		error(400, 'Bad Request');
	}

	const { error: responseError } = await supabase
		.from('conversations')
		.update({ label: requestData.label })
		.eq('id', requestData.id);

	if (responseError) {
		console.log(
			`error updating conversation,  error: ${responseError?.code}: ${responseError?.message}`
		);
		error(500, { message: 'Internal Server Error' });
	}

	return new Response(null, { status: 204 });
}
