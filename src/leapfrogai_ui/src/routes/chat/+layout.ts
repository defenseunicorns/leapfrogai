import type { LayoutLoad } from './$types';
import { browser } from '$app/environment';
import { filesStore, threadsStore } from '$stores';
import type { LFAssistant } from '$lib/types/assistants';
import type { FileObject } from 'openai/resources/files';
import { convertFileObjectToFileRows } from '$helpers/fileHelpers';
import type { FileRow } from '$lib/types/files';

// Load the store with the threads fetched by the +layout.server.ts (set store on the client side only)
// This only runs when the app is first loaded (because it's a higher level layout)
// After this load, the app keeps the store in sync with data changes and we don't
// re-fetch all that data from the server
// The same applies to files, we keep track of them in a store
export const load: LayoutLoad = async ({ fetch, data, depends }) => {
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
    let fileRows: FileRow[] = [];
    if (files && files.length > 0) {
      fileRows = convertFileObjectToFileRows(files);
    }

    filesStore.setFiles(fileRows);
    threadsStore.setThreads(data?.threads || []);
  }
  return { assistants };
};
