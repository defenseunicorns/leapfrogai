import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';

export const GET: RequestHandler = async ({ url, locals: { session } }) => {
    if (!session) {
        error(401, 'Unauthorized');
    }

    const id = url.searchParams.get('id');

    if (!id) error(400, 'Invalid request');
    try {
        const openai = getOpenAiClient(session.access_token);

        const vectorStoreFilesPage = await openai.beta.vectorStores.files.list(id)
        return json(vectorStoreFilesPage);
    } catch (e) {
        console.error(`Error getting vector store: ${e}`);
        error(500, 'Error getting vector store');
    }
};
