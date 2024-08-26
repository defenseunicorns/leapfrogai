import { expect, type Page } from '@playwright/test';
import OpenAI from 'openai';
import type { Profile } from '$lib/types/profile';
import { LONG_RESPONSE_PROMPT, SHORT_RESPONSE_PROMPT, supabase } from './helpers';
import type { LFThread } from '$lib/types/threads';

export const clickToDeleteThread = async (page: Page, label: string) => {
  await page.getByTestId(`thread-menu-btn-${label}`).click();
  await page.getByRole('button', { name: /delete/i }).click();
  const deleteBtns = await page.getByRole('button', { name: /delete/i }).all();
  await deleteBtns[1].click(); // confirm delete in modal
  await expect(page.getByTestId(`thread-menu-btn-${label}`)).toHaveCount(0);
};

export const sendMessage = async (page: Page, message = 'Who are Defense Unicorns?') => {
  await page.getByTestId('chat-input').fill(message);
  await page.click('button[type="submit"]');
};

export const getLastUrlParam = (page: Page) => {
  const urlParts = new URL(page.url()).pathname.split('/');
  return urlParts[urlParts.length - 1];
};
export const deleteActiveThread = async (page: Page, openAIClient: OpenAI) => {
  const threadId = getLastUrlParam(page);

  if (threadId && threadId !== 'chat') {
    await deleteThread(threadId, openAIClient);
  }
};

const getUserId = async () => {
  const listUsers = await supabase.auth.admin.listUsers();
  let userId = '';
  for (const user of listUsers.data.users) {
    if (user.email === process.env.USERNAME) {
      userId = user.id;
    }
  }
  return userId;
};

const getUserThreadIds = async (userId: string) => {
  const { data: profile } = await supabase
    .from('profiles')
    .select(`*`)
    .eq('id', userId)
    .returns<Profile[]>()
    .single();

  return profile?.thread_ids || [];
};

export const deleteThread = async (id: string, openAIClient: OpenAI) => {
  await openAIClient.beta.threads.del(id);
  const userId = await getUserId();
  const threadIds = await getUserThreadIds(userId);

  const updatedThreadIds = threadIds.filter((existingId) => existingId !== id);

  await supabase.from('profiles').update({ thread_ids: updatedThreadIds }).eq('id', userId);
};
export const waitForResponseToComplete = async (page: Page) => {
  await expect(page.getByTestId('cancel message')).toHaveCount(1, { timeout: 60000 });
  await expect(page.getByTestId('cancel message')).toHaveCount(0, { timeout: 60000 });
  await expect(page.getByTestId('send message')).toHaveCount(1, { timeout: 60000 });
};

export const deleteAllTestThreadsWithApi = async (openAIClient: OpenAI) => {
  try {
    const userId = await getUserId();
    const threadIds = await getUserThreadIds(userId);
    for (const id of threadIds) {
      let thread: LFThread | undefined = undefined;
      try {
        thread = (await openAIClient.beta.threads.retrieve(id)) as LFThread;
      } catch (e) {
        console.error(`Error fetching thread: ${id}`);
        console.error(`Error: ${e}`);
      }

      if (
        thread?.metadata?.label.includes(SHORT_RESPONSE_PROMPT) ||
        thread?.metadata?.label.includes(LONG_RESPONSE_PROMPT)
      ) {
        try {
          await openAIClient.beta.threads.del(id);
          const updatedThreadIds = threadIds?.filter((existingId) => existingId !== id);
          await supabase.from('profiles').update({ thread_ids: updatedThreadIds }).eq('id', userId);
        } catch (e) {
          console.error(`Error deleting thread: ${threadIds}`);
          console.error(`Error: ${e}`);
        }
      }
    }
  } catch (e) {
    console.error(`Error deleting test threads`, e);
  }
};
