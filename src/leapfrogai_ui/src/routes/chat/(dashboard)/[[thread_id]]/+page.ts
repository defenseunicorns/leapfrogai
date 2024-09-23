import type { PageLoad } from './$types';
import { browser } from '$app/environment';
import type { LFThread } from '$lib/types/threads';
import { threadsStore } from '$stores';

export const load: PageLoad = async ({ params, fetch }) => {
  const promises = [fetch('/api/assistants'), fetch('/api/files')];

  if (params.thread_id) promises.push(fetch(`/api/threads/${params.thread_id}`));

  const promiseResponses = await Promise.all(promises);

  const assistants = await promiseResponses[0].json();
  const files = await promiseResponses[1].json();

  let thread: LFThread | undefined = undefined;
  if (params.thread_id) {
    thread = await promiseResponses[2].json();
  }

  if (browser) {
    if (thread) {
      // update store with latest thread fetched by page data
      threadsStore.updateThread(thread);
    }
  }

  return { thread, assistants, files };
};
