import { error } from '@sveltejs/kit';
import { openai } from '$lib/server/constants';

export async function POST({ request, locals: { getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }
  console.log(request)

  // const uploadedFile = await openai.files.create({
  //   file: file,
  //   purpose: 'assistants'
  // });
}
