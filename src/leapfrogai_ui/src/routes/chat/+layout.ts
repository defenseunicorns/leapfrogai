import type { LayoutLoad } from './$types';
import { browser } from '$app/environment';
import { assistantsStore, filesStore, threadsStore, uiStore } from '$stores';
import type { LFAssistant } from '$lib/types/assistants';
import type { FileObject } from 'openai/resources/files';
import type { LFThread } from '$lib/types/threads';
import type { LFFileObject } from '$lib/types/files';
import { convertFileObjectToLFFileObject } from '$helpers/fileHelpers';

export const load: LayoutLoad = async ({ fetch, data }) => {
  const promises: Array<Promise<Response>> = [
    fetch('/api/assistants'),
    fetch('/api/files'),
    fetch('/api/threads')
  ];
  const [assistantRes, filesRes, threadsRes] = await Promise.all(promises);
  const assistants = (await assistantRes.json()) as LFAssistant[];
  const files = (await filesRes.json()) as FileObject[];
  const threads = (await threadsRes.json()) as LFThread[];
  if (browser) {
    uiStore.setIsUsingOpenAI(data?.isUsingOpenAI);
    // Convert files to LFFileObjects and set in store
    let lfFileObjects: LFFileObject[] = [];
    if (files && files.length > 0) {
      lfFileObjects = convertFileObjectToLFFileObject(files);
    }
    filesStore.setFiles(lfFileObjects);
    threadsStore.setThreads(threads || []);
    assistantsStore.setAssistants(assistants || []);
  }
  return { assistants, files, threads };
};
