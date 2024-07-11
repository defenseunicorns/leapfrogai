import OpenAI from 'openai';
import { expect, type Page } from '@playwright/test';
import { getFakeAssistantInput } from '$testUtils/fakeData';
import type { AssistantCreateParams } from 'openai/resources/beta/assistants';
import type { AssistantInput, LFAssistant } from '$lib/types/assistants';
import { supabase } from './helpers';

// Note - this will not apply the temperature slider value provided, it only clicks on the 0.5 increment
export const createAssistant = async (assistantInput: AssistantInput, page: Page) => {
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
export const deleteAllAssistants = async (openAIClient: OpenAI) => {
  try {
    const myAssistants = await openAIClient.beta.assistants.list();
    for (const assistant of myAssistants.data) {
      await deleteAssistantWithApi(assistant.id, openAIClient);
    }
  } catch (e) {
    console.error(`Error deleting test assistants`, e);
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
export const createAssistantWithApi = async (openAIClient: OpenAI) => {
  const fakeAssistantInput = getFakeAssistantInput();
  const assistantInput: AssistantCreateParams = {
    name: fakeAssistantInput.name,
    description: fakeAssistantInput.description,
    instructions: fakeAssistantInput.instructions,
    temperature: fakeAssistantInput.temperature,
    model: process.env.DEFAULT_MODEL!,
    metadata: {
      pictogram: 'Default'
    }
  };

  return (await openAIClient.beta.assistants.create(assistantInput)) as LFAssistant;
};
export const deleteAssistantWithApi = async (id: string, openAIClient: OpenAI) => {
  await openAIClient.beta.assistants.del(id);
};
export const deleteAssistant = async (name: string, page: Page) => {
  await page.getByTestId(`assistant-tile-${name}`).getByTestId('overflow-menu').click();
  // click overflow menu delete btn
  await page.getByRole('menuitem', { name: 'Delete' }).click();
  // click modal actual delete btn
  await page.getByRole('button', { name: 'Delete' }).click();
};

export const deleteAssistantAvatars = async () => {
  await supabase.storage.emptyBucket('assistant_avatars');
};
