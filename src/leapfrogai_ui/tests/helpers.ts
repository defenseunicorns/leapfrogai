import { expect, type Page } from '@playwright/test';
import { faker } from '@faker-js/faker';
import { createClient } from '@supabase/supabase-js';
import type { AssistantInput, LFAssistant } from '$lib/types/assistants';
import OpenAI from 'openai';
import type { Profile } from '$lib/types/profile';
import { getFakeAssistantInput } from '$testUtils/fakeData';
import * as fs from 'node:fs';

const supabase = createClient(process.env.PUBLIC_SUPABASE_URL!, process.env.SERVICE_ROLE_KEY!);

// These messages result in faster responses to avoid timeout issues
export const getSimpleMathQuestion = () => {
  const operations = [
    { operation: 'add', preposition: 'to' },
    { operation: 'subtract', preposition: 'from' },
    { operation: 'divide', preposition: 'by' },
    { operation: 'multiply', preposition: 'by' }
  ];
  const randomOperation = faker.helpers.arrayElement(operations);
  const randomNumber1 = faker.number.int({ min: 1, max: 1000 });
  const randomNumber2 = faker.number.int({ min: 1, max: 1000 });
  return `${randomOperation.operation} ${randomNumber1} ${randomOperation.preposition} ${randomNumber2}`;
};

export const openai = new OpenAI({
  apiKey: process.env.LEAPFROGAI_API_KEY ?? '',
  baseURL: process.env.LEAPFROGAI_API_BASE_URL
});

export const loadChatPage = async (page: Page) => {
  await page.goto('/chat');
  await page.waitForURL('/chat');
  await expect(page).toHaveTitle('LeapfrogAI - Chat');
};

export const clickToDeleteThread = async (page: Page, label: string) => {
  await page.getByTestId(`overflow-menu-${label}`).click();
  await page.getByTestId(`overflow-menu-delete-${label}`).click();

  await page.locator('button:text("Delete")').click();
  await expect(page.getByTestId(`overflow-menu-${label}`)).toHaveCount(0);
};

export const sendMessage = async (page: Page, message = 'Who are Defense Unicorns?') => {
  await page.getByLabel('message input').fill(message);
  await page.click('button[type="submit"]');
};

// Note - this will not apply the temperature slider value provided, it only clicks on the 0.5 increment
export const createAssistant = async (page: Page, assistantInput: AssistantInput) => {
  await page.goto('/chat/assistants-management/new');
  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('description').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);
  await page.locator('.bx--slider__track').click();

  // Wait for modal save button to disappear if avatar modal was open
  const saveButtons = page.getByRole('button', { name: 'Save' });
  await expect(saveButtons).toHaveCount(1);

  await saveButtons.click();
};

export const deleteActiveThread = async (page: Page) => {
  const urlParts = new URL(page.url()).pathname.split('/');
  const threadId = urlParts[urlParts.length - 1];

  if (threadId && threadId !== 'chat') {
    await deleteThread(threadId);
  }
};
export const deleteThread = async (id: string) => {
  await openai.beta.threads.del(id);
  const listUsers = await supabase.auth.admin.listUsers();
  let userId = '';
  for (const user of listUsers.data.users) {
    if (user.email === process.env.USERNAME) {
      userId = user.id;
    }
  }
  const { data: profile } = await supabase
    .from('profiles')
    .select(`*`)
    .eq('id', userId)
    .returns<Profile[]>()
    .single();

  const updatedThreadIds = profile?.thread_ids.filter((existingId) => existingId !== id);

  await supabase.from('profiles').update({ thread_ids: updatedThreadIds }).eq('id', userId);
};

export const waitForResponseToComplete = async (page: Page) => {
  await expect(page.getByTestId('cancel message')).toHaveCount(1, { timeout: 30000 });
  await expect(page.getByTestId('cancel message')).toHaveCount(0, { timeout: 30000 });
  await expect(page.getByTestId('send message')).toHaveCount(1, { timeout: 30000 });
};

export const deleteAllAssistants = async () => {
  const myAssistants = await openai.beta.assistants.list();
  for (const assistant of myAssistants.data) {
    await deleteAssistantWithApi(assistant.id);
  }
};

export const attachAvatarImage = async (page: Page, imageName: string) => {
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.locator('label').filter({ hasText: 'Upload from computer' }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles(`./tests/fixtures/${imageName}.png`);
};

export const uploadAvatar = async (page: Page, imageName = 'Doug') => {
  await page.getByText('Upload', { exact: true }).click();

  await attachAvatarImage(page, imageName);

  const imageUploadContainer = page.getByTestId('image-upload-avatar');
  const hasImage = await imageUploadContainer.evaluate((node) => {
    return window.getComputedStyle(node).backgroundImage;
  });
  expect(hasImage).toBeDefined();
};

export const createAssistantWithApi = async () => {
  const fakeAssistantInput = getFakeAssistantInput();
  const assistantInput = {
    name: fakeAssistantInput.name,
    description: fakeAssistantInput.description,
    instructions: fakeAssistantInput.instructions,
    temperature: fakeAssistantInput.temperature,
    model: process.env.DEFAULT_MODEL!,
    metadata: {
      pictogram: 'Default'
    }
  };

  return (await openai.beta.assistants.create(assistantInput)) as LFAssistant;
};

export const deleteAssistantWithApi = async (id: string) => {
  await openai.beta.assistants.del(id);
};

export const uploadFileWithApi = async (fileName = 'test.pdf') => {
  const file = fs.createReadStream(`./tests/fixtures/${fileName}`);

  return openai.files.create({
    file: file,
    purpose: 'assistants'
  });
};
export const deleteFileWithApi = async (id: string) => {
  return openai.files.del(id);
};

export const uploadFile = async (page: Page, filename = 'test.pdf', btnName = 'upload') => {
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByRole('button', { name: btnName }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles(`./tests/fixtures/${filename}`);
};

export const deleteAssistant = async (page: Page, name: string) => {
  await page.goto(`/chat/assistants-management`);
  await page.getByTestId(`assistant-tile-${name}`).getByTestId('overflow-menu').click();
  // click overflow menu delete btn
  await page.getByRole('menuitem', { name: 'Delete' }).click();
  // click modal actual delete btn
  await page.getByRole('button', { name: 'Delete' }).click();
};

export const deleteFirstFile = async (page: Page) => {
  await page.goto(`/chat/file-management`);
  const checkboxes = await page.getByRole('checkbox').all();
  await checkboxes[1].check(); // first checkbox is for selecting all, pick the second one
  await page.getByText('Delete').click();
};

export const deleteTestFilesWithApi = async () => {
  const list = await openai.files.list();
  const idsToDelete: string[] = [];
  for await (const file of list) {
    if (file.filename.startsWith('test')) {
      idsToDelete.push(file.id);
    }
  }

  const promises = [];
  for (const id of idsToDelete) {
    promises.push(openai.files.del(id));
  }
  await Promise.all(promises);
};
