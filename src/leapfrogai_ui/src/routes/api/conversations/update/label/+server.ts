import { error } from '@sveltejs/kit';

export async function PUT({ request, locals: { supabase } }) {
	const { id, label } = await request.json();

	// TODO - for validation, ensure max length MAX_LABEL_SIZE

	const { error: responseError } = await supabase
		.from('conversations')
		.update({ label: label })
		.eq('id', id);

	if (responseError) {
		console.log(
			`error updating conversation,  error: ${responseError?.code}: ${responseError?.message}`
		);
		error(500, { message: 'Internal Server Error' });
	}

	return new Response(null, { status: 204 });
}
