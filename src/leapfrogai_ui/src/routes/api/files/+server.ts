import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';
import type { FileObject } from 'openai/resources/files';

export const GET: RequestHandler = async ({ locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  const openai = getOpenAiClient(session.access_token);

  const list = await openai.files.list();

  const files = list.data as FileObject[];

  return json(files ?? []);
};
