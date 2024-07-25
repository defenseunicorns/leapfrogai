import OpenAI from 'openai';
import { expect, type Page } from '@playwright/test';
import { getFakeAssistantInput } from '../../testUtils/fakeData';
import type { AssistantCreateParams } from 'openai/resources/beta/assistants';
import type { AssistantInput, LFAssistant } from '../../src/lib/types/assistants';
import { supabase } from './helpers';

// Note - this will not apply the temperature slider value provided, it only clicks on the 0.5 increment
export const createAssistant = async (assistantInput: AssistantInput, page: Page) => {
  await page.goto('/chat/assistants-management/new');
  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('tagline').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  const slider = page.getByRole('slider');
  const sliderButton = slider.getByRole('button');
  const box = await sliderButton.boundingBox();
  if (box) {
    const startX = box.x + box.width / 2;
    const startY = box.y + box.height / 2;
    const endX = startX + 100; // adjust as needed
    await page.mouse.move(startX, startY);
    await page.mouse.down();
    await page.mouse.move(endX, startY, { steps: 10 }); // Drag to the new position
    await page.mouse.up();
  }

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

type CreateAssistantWithApiParams = {
  assistantInput?: AssistantInput;
  openAIClient: OpenAI;
};
export const createAssistantWithApi = async (params: CreateAssistantWithApiParams) => {
  const { assistantInput = getFakeAssistantInput(), openAIClient } = params;

  const withFiles = assistantInput.data_sources && assistantInput.data_sources.length > 0;

  const assistantCreateParams: AssistantCreateParams = {
    name: assistantInput.name,
    description: assistantInput.description,
    instructions: assistantInput.instructions,
    temperature: assistantInput.temperature,
    model: process.env.DEFAULT_MODEL!,
    metadata: {
      pictogram: 'Default'
    },
    ...(withFiles && {
      tools: [{ type: 'file_search' }],
      tool_resources: {
        file_search: {
          vector_stores: [{ file_ids: assistantInput.data_sources as string[] }]
        }
      }
    })
  };

  return (await openAIClient.beta.assistants.create(assistantCreateParams)) as LFAssistant;
};
export const deleteAssistantWithApi = async (id: string, openAIClient: OpenAI) => {
  await openAIClient.beta.assistants.del(id);
};

export const editAssistantCard = async (name: string, page: Page) => {
  const assistantCard = page.getByTestId(`assistant-card-${name}`);
  await assistantCard.getByTestId('assistant-edit-icon').click();
  // click edit menu delete btn
  await assistantCard
    .getByTestId('assistant-card-dropdown')
    .getByRole('button', { name: /edit/i })
    .click();
};

export const deleteAssistantCard = async (name: string, page: Page) => {
  const assistantCard = page.getByTestId(`assistant-card-${name}`);
  await assistantCard.getByTestId('assistant-edit-icon').click();
  // click edit menu delete btn
  await assistantCard.getByRole('button', { name: /delete/i }).click();
  // click modal confirmation delete btn
  await page
    .getByTestId('delete-assistant-modal')
    .getByRole('button', { name: /delete/i })
    .click();
};

export const deleteAssistantAvatars = async () => {
  await supabase.storage.emptyBucket('assistant_avatars');
};
