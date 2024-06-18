import type { LFThread } from '$lib/types/threads';

export const load = async ({ params, fetch, depends }) => {
  depends('lf:thread');
  const promises = [fetch('/api/assistants'), fetch('/api/files')];

  if (params.thread_id) promises.push(fetch(`/api/threads/${params.thread_id}`));

  const promiseResponses = await Promise.all(promises);

  const assistants = await promiseResponses[0].json();
  const files = await promiseResponses[1].json();

  let thread: LFThread | undefined = undefined;
  if (params.thread_id) {
    thread = await promiseResponses[2].json();
  }

  return { thread, assistants, files };
};
