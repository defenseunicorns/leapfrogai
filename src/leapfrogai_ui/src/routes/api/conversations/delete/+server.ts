import { error, redirect } from '@sveltejs/kit';
import { uuidSchema } from '../../../../schemas/chat';

export async function DELETE({ request, locals: { supabase, getSession } }) {

	const session = await getSession();
	if (!session) {
		error(401, 'Unauthorized');
	}

	let requestData: { conversationId: string };

	// Validate request body
	try {
		requestData = await request.json();
		const isValid = await uuidSchema.isValid(requestData);
		if (!isValid) error(400, 'Bad Request');
	} catch {
		error(400, 'Bad Request');
	}

	const { error: responseError } = await supabase
		.from('conversations')
		.delete()
		.eq('id', requestData.conversationId);

	if (responseError) {
		console.log(
			`error deleting conversation, error status: ${responseError?.code}: ${responseError?.message}`
		);
		error(500, 'Error deleting conversation');
	}

	return new Response(undefined, { status: 204 });
}
