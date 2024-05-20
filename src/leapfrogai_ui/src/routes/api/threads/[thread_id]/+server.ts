import { error, json } from '@sveltejs/kit';
import OpenAI from 'openai';
import { env } from '$env/dynamic/private';
import {openai} from "$lib/server/constants";



export async function GET({ request, params, locals: { getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  const thread = await openai.beta.threads.retrieve(params.thread_id);
  return json(thread);
}
