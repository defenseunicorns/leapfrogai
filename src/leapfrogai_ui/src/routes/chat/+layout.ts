import { browser } from '$app/environment';
import { filesStore, threadsStore } from '$stores';
import type { LFAssistant } from '$lib/types/assistants';
import type { FileObject } from 'openai/resources/files';
import type { FileRow } from '$lib/types/files';

// Load the store with the threads fetched by the +layout.server.ts (set store on the client side only)
// This only runs when the app is first loaded (because it's a higher level layout)
// After this load, the app keeps the store in sync with data changes and we don't
// re-fetch all that data from the server
// The same applies to files, we keep track of them in a store
export const load = async ({ fetch, data, depends }) => {
  depends('lf:assistants');
  depends('lf:files');

  const promises: [Promise<Response>, Promise<Response>] = [
    fetch('/api/assistants'),
    fetch('/api/files')
  ];
  const [assistantRes, filesRes] = await Promise.all(promises);
  const assistants = (await assistantRes.json()) as LFAssistant[];
  const files = (await filesRes.json()) as FileObject[];

  if (browser) {
    const fileRows: FileRow[] = files.map((file) => ({
      id: file.id,
      filename: file.filename,
      created_at: file.created_at,
      status: 'complete'
    }));
    filesStore.setFiles(fileRows);
    threadsStore.setThreads(data?.threads || []);
  }

  return { assistants };
};
