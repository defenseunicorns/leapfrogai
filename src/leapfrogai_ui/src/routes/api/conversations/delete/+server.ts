import { error, json } from '@sveltejs/kit';

export async function DELETE({ request, locals: { supabase } }) {
	const requestData = await request.json();

	const id: string = requestData.conversationId;

	const { error: responseError } = await supabase.from('conversations').delete().eq('id', id);

	if (responseError) {
		console.log(
			`error deleting conversation, error: ${responseError?.code}: ${responseError?.message}`
		);
		error(500, 'Error deleting conversation');
	}

	return json({ message: 'success' });
}
