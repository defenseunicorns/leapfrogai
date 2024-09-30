import { expect, test } from './fixtures';
import { getSimpleMathQuestion } from './helpers/helpers';
import { getFakeAssistantInput } from '../testUtils/fakeData';
import type { ActionResult } from '@sveltejs/kit';
import {
  createAssistant,
  createAssistantWithApi,
  deleteAssistantCard,
  deleteAssistantWithApi,
  editAssistantCard,
  getAssistantWithApi
} from './helpers/assistantHelpers';
import { deleteActiveThread, getLastUrlParam, sendMessage } from './helpers/threadHelpers';
import {
  loadAssistantsManagementPage,
  loadChatPage,
  loadNewAssistantPage
} from './helpers/navigationHelpers';
import { ERROR_GETTING_ASSISTANT_MSG_TOAST } from '$constants/toastMessages';
import { ASSISTANT_ERROR_MSG } from '$constants/errors';

const newMessage1 = getSimpleMathQuestion();

test('it navigates to the assistants page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByTestId('header-settings-btn').click();
  await page.getByText('Assistants Management').click();

  await expect(page).toHaveTitle('LeapfrogAI - Assistants Management');
});

test('it has a button that navigates to the new assistant page', async ({ page }) => {
  await loadAssistantsManagementPage(page);
  await page.getByRole('button', { name: 'New Assistant' }).click();
  await page.waitForURL('**/assistants-management/new');
  await expect(page).toHaveTitle('LeapfrogAI - New Assistant');
});

test('it creates an assistant and navigates back to the management page', async ({
  page,
  openAIClient
}) => {
  const assistantInput = getFakeAssistantInput();

  await createAssistant(assistantInput, page);

  await expect(page.getByText('Assistant Created')).toBeVisible({ timeout: 10000 });
  await page.waitForURL('/chat/assistants-management');
  await expect(page.getByTestId(`assistant-card-${assistantInput.name}`)).toBeVisible();

  // Verify created assistant has the correct attributes
  await editAssistantCard(assistantInput.name, page);
  await page.waitForURL('/chat/assistants-management/edit/**/*');
  const assistantId = getLastUrlParam(page);
  const assistant = await getAssistantWithApi(assistantId, openAIClient);
  expect(assistant.name).toEqual(assistantInput.name);
  expect(assistant.description).toEqual(assistantInput.description);
  expect(assistant.instructions).toEqual(assistantInput.instructions);
  expect(assistant.temperature).toBeCloseTo(assistantInput.temperature, 0.1);

  // cleanup
  await deleteAssistantWithApi(assistantId, openAIClient);
});

test('displays an error toast when there is an error creating an assistant and remains on the assistant page (form submission returns 200)', async ({
  page
}) => {
  const assistantInput = getFakeAssistantInput();

  await page.route('*/**/chat/assistants-management/new', async (route) => {
    if (route.request().method() === 'POST') {
      // this returns a 200, but result.type === 'failure'
      const result: ActionResult = {
        type: 'failure',
        status: 500
      };

      await route.fulfill({ json: result });
    } else {
      const response = await route.fetch();
      await route.fulfill({ response });
    }
  });

  await createAssistant(assistantInput, page);

  await expect(page.getByText('Error Creating Assistant')).toBeVisible();
});
test('displays an error toast when there is an error creating an assistant and remains on the assistant page (form submission returns 500)', async ({
  page
}) => {
  const assistantInput = getFakeAssistantInput();

  await page.route('*/**/chat/assistants-management/new', async (route) => {
    if (route.request().method() === 'POST') {
      // this returns a 500 and result.type === 'error'
      await route.abort();
    } else {
      const response = await route.fetch();
      await route.fulfill({ response });
    }
  });

  await createAssistant(assistantInput, page);

  await expect(page.getByText('Error Creating Assistant')).toBeVisible();
});
test('displays an error toast when there is an error editing an assistant and remains on the assistant page', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  const newAssistantAttributes = getFakeAssistantInput();

  await loadAssistantsManagementPage(page);

  await editAssistantCard(assistant.name!, page);

  await page.waitForURL('/chat/assistants-management/edit/**/*');

  await page.route(`*/**/chat/assistants-management/edit/${assistant.id}`, async (route) => {
    if (route.request().method() === 'POST') {
      // this returns a 500 and result.type === 'error'
      await route.abort('failed');
    } else {
      const response = await route.fetch();
      await route.fulfill({ response });
    }
  });

  await page.getByLabel('name').fill(newAssistantAttributes.name);

  // Wait for modal save button to disappear if avatar modal was open
  const saveButtons = page.getByRole('button', { name: 'Save' });
  await expect(saveButtons).toHaveCount(1);

  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText('Error Editing Assistant')).toBeVisible();

  await page.waitForURL(`/chat/assistants-management/edit/${assistant.id}`);

  // cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
});

test('it can search for assistants', async ({ page, openAIClient }) => {
  const assistant1 = await createAssistantWithApi({ openAIClient });
  const assistant2 = await createAssistantWithApi({ openAIClient });

  await loadAssistantsManagementPage(page);

  const searchBox = page.getByRole('textbox', {
    name: /search/i
  });
  await expect(searchBox).toBeVisible();
  // Search by name
  await searchBox.fill(assistant1.name!);

  await expect(page.getByTestId(`assistant-card-${assistant2.name}`)).not.toBeVisible();
  await expect(page.getByTestId(`assistant-card-${assistant1.name}`)).toBeVisible();

  // search by description
  await searchBox.clear();
  await searchBox.fill(assistant2.description!);

  await expect(page.getByTestId(`assistant-card-${assistant2.name!}`)).toBeVisible();
  await expect(page.getByTestId(`assistant-card-${assistant1.name!}`)).not.toBeVisible();

  // Search by instructions
  await searchBox.fill(assistant1.instructions!);

  await expect(page.getByTestId(`assistant-card-${assistant2.name}`)).not.toBeVisible();
  await expect(page.getByTestId(`assistant-card-${assistant1.name}`)).toBeVisible();

  // cleanup
  await searchBox.clear();
  await deleteAssistantWithApi(assistant1.id, openAIClient);
  await deleteAssistantWithApi(assistant2.id, openAIClient);
});

test('it can navigate to the last visited thread with breadcrumbs', async ({
  page,
  openAIClient
}) => {
  const newMessage = getSimpleMathQuestion();
  await page.goto('/chat');
  await sendMessage(page, newMessage);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(2);

  const threadId = getLastUrlParam(page);

  await page.getByTestId('header-settings-btn').click();
  await page.getByText('Assistants Management').click();
  await page.getByRole('button', { name: 'New Assistant' }).click();
  await page.waitForURL('/chat/assistants-management/new');
  await page
    .getByTestId('breadcrumbs')
    .getByRole('link', { name: 'Assistants Management' })
    .click();
  await page.waitForURL('/chat/assistants-management');
  await page.getByTestId('breadcrumbs').getByRole('link', { name: 'Chat' }).click();
  await page.waitForURL(`/chat/${threadId}`);

  // Cleanup
  await deleteActiveThread(page, openAIClient);
});

test('it validates input', async ({ page }) => {
  await loadNewAssistantPage(page);
  await page.getByLabel('name').fill('my assistant');
  const saveButton = page.getByRole('button', { name: 'Save' });

  await saveButton.click();

  await expect(page.getByText('This field is required. Please enter a tagline.')).toHaveCount(1);
  await expect(page.getByText('This field is required. Please enter instructions.')).toHaveCount(1);

  // Test client side validation - errors disappear live without have to click save
  await page.getByLabel('tagline').fill('my description');

  await page.getByPlaceholder("You'll act as...").fill('my instructions');
  await expect(page.getByText('This field is required. Please enter a tagline.')).toHaveCount(0);
  await expect(page.getByText('This field is required. Please enter instructions.')).toHaveCount(0);
});

test('it confirms you want to navigate away if you have changes', async ({ page }) => {
  await loadNewAssistantPage(page);
  await page.getByLabel('name').fill('my assistant');

  await page.getByRole('link', { name: 'Assistants Management' }).click();

  await expect(
    page.getByText(
      'You have unsaved changes. Do you want to leave this page? Unsaved changes will be deleted.'
    )
  ).toBeVisible();
  expect(page.url()).toContain('/chat/assistants-management/new');
});

test('it DOES NOT confirm you want to navigate away if you DONT have changes', async ({ page }) => {
  await loadNewAssistantPage(page);
  await page.getByRole('link', { name: 'Assistants Management' }).click();

  await page.waitForURL('/chat/assistants-management');
});

test('it DOES NOT confirm you want to navigate away if you click the cancel button', async ({
  page
}) => {
  await loadNewAssistantPage(page);
  await page.getByLabel('name').fill('my assistant');

  await page.getByRole('button', { name: 'Cancel' }).click();

  await page.waitForURL('/chat/assistants-management');
});

test('it allows you to edit an assistant', async ({ page, openAIClient }) => {
  const pictogramName = 'Analytics';
  const assistant1 = await createAssistantWithApi({ openAIClient });
  const newAssistantAttributes = getFakeAssistantInput();

  await loadAssistantsManagementPage(page);

  await editAssistantCard(assistant1.name!, page);

  await page.getByLabel('name').fill(newAssistantAttributes.name);
  await page.getByLabel('tagline').fill(newAssistantAttributes.description);
  await page.getByPlaceholder("You'll act as...").fill(newAssistantAttributes.instructions);

  await page.getByTestId('mini-avatar-container').click();
  await page.getByTestId(`pictogram-${pictogramName}`).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  // Wait for modal save button to disappear if avatar modal was open
  const saveButtons = page.getByRole('button', { name: 'Save' });
  await expect(saveButtons).toHaveCount(1);

  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText('Assistant Updated')).toBeVisible();
  await expect(page.getByTestId(`assistant-card-${newAssistantAttributes.name}`)).toBeVisible();

  //cleanup
  await deleteAssistantWithApi(assistant1.id, openAIClient);
});

test("it populates the assistants values when editing an assistant's details", async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });

  await loadAssistantsManagementPage(page);

  await editAssistantCard(assistant.name!, page);

  await expect(page.getByLabel('name')).toHaveValue(assistant.name!);
  await expect(page.getByLabel('tagline')).toHaveValue(assistant.description!);
  await expect(page.getByPlaceholder("You'll act as...")).toHaveValue(assistant.instructions!);

  //cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
});

test('it can delete assistants', async ({ page, openAIClient }) => {
  const assistant = await createAssistantWithApi({ openAIClient });

  await loadAssistantsManagementPage(page);

  await deleteAssistantCard(assistant.name!, page);

  await expect(page.getByText(`${assistant.name} Assistant deleted.`)).toBeVisible();
});

test('displays a toast if there is an error deleting an assistant and the call throws', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadAssistantsManagementPage(page);
  await page.route('*/**/api/assistants/delete', async (route) => {
    await route.abort();
  });
  await deleteAssistantCard(assistant.name!, page);
  await expect(page.getByText('Error deleting Assistant.')).toBeVisible();

  //cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
});
test('displays a toast if there is an error deleting an assistant and response is not 200', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadAssistantsManagementPage(page);
  await page.route('*/**/api/assistants/delete', async (route) => {
    await route.fulfill({ status: 500 });
  });
  await deleteAssistantCard(assistant.name!, page);
  await expect(page.getByText('Error deleting Assistant.')).toBeVisible();

  //cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
});

// Note - these error cases do not test all edge cases. ex. completed response comes back empty, /chat/assistants
// partially completes then fails, stream fails, etc...
test('displays an error toast if /chat/assistants throws while getting a response from an assistant', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadChatPage(page);

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  await page.route('*/**/chat/assistants', async (route) => {
    await route.abort('failed');
  });
  await sendMessage(page, newMessage1);

  await expect(page.getByText(ERROR_GETTING_ASSISTANT_MSG_TOAST().title)).toBeVisible();
  await expect(page.getByText(ASSISTANT_ERROR_MSG)).toBeVisible();
});

test('displays an error toast if /chat/assistants returns a 500 when getting a response from an assistant', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadChatPage(page);

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  await page.route('*/**/chat/assistants', async (route) => {
    await route.fulfill({ status: 500 });
  });
  await sendMessage(page, newMessage1);

  await expect(page.getByText(ERROR_GETTING_ASSISTANT_MSG_TOAST().title)).toBeVisible();
  await expect(page.getByText(ASSISTANT_ERROR_MSG)).toBeVisible();
});

test('displays an error toast if /chat/assistants returns a 200 with no body when getting a response from an assistant', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadChatPage(page);

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  await page.route('*/**/chat/assistants', async (route) => {
    await route.fulfill({ status: 200 });
  });
  await sendMessage(page, newMessage1);

  await expect(page.getByText(ERROR_GETTING_ASSISTANT_MSG_TOAST().title)).toBeVisible();
  await expect(page.getByText(ASSISTANT_ERROR_MSG)).toBeVisible();
});
