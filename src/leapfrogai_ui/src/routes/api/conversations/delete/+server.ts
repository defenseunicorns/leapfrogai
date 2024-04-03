import { error } from '@sveltejs/kit';
import { uuidSchema } from '../../../../schemas/chat';

export async function DELETE({ request, locals: { supabase } }) {
	let id: string;
	try {
		const requestData = await request.json();
		id = requestData.conversationId;
	} catch (e) {
		error(400, { message: 'Bad Request' });
	}

	const isValid = await uuidSchema.isValid(id);
	if (!isValid) error(400, 'Bad Request');

	const { error: responseError } = await supabase.from('conversations').delete().eq('id', id);

	if (responseError) {
		console.log(
			`error deleting conversation, error: ${responseError?.code}: ${responseError?.message}`
		);
		error(500, 'Error deleting conversation');
	}

	return new Response(undefined, { status: 204 });
}
