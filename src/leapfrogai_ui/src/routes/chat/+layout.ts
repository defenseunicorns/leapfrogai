import type { LayoutLoad } from './$types';
import { browser } from '$app/environment';
import { uiStore } from '$stores';
import type { LFAssistant } from '$lib/types/assistants';
import type { FileObject } from 'openai/resources/files';
import type { LFThread } from '$lib/types/threads';

export const load: LayoutLoad = async ({ fetch, data, depends }) => {
  depends('lf:assistants');
  depends('lf:files');
  depends('lf:threads');

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
  }
  return { assistants, files, threads };
};
