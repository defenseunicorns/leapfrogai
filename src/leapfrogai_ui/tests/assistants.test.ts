import { expect, test } from './fixtures';
import { createAssistant, deleteAssistantByName, loadChatPage } from './helpers';
import { getFakeNewAssistantInput } from '../testUtils/fakeData';
import type { ActionResult } from '@sveltejs/kit';

test('it navigates to the assistants page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByLabel('Settings').click();
  await page.getByText('Assistants Management').click();

  await expect(page).toHaveTitle('LeapfrogAI - Assistants');
});

test('it has a button that navigates to the new assistant page', async ({ page }) => {
  await page.goto('/chat/assistants-management');

  await page.getByRole('button', { name: 'New Assistant' }).click();
  await page.waitForURL('**/assistants-management/new');
  await expect(page).toHaveTitle('LeapfrogAI - New Assistant');
});

test('it creates an assistant and navigates back to the management page', async ({ page }) => {
  const assistantInput = getFakeNewAssistantInput();

  await createAssistant(page, assistantInput);

  await page.waitForURL('/chat/assistants-management');
  await expect(page.getByText(assistantInput.name)).toBeVisible();

  // cleanup
  await deleteAssistantByName(assistantInput.name);
});

test('displays an error toast when there is an error creating an assistant and remains on the assistant page', async ({
  page
}) => {
  const assistantInput = getFakeNewAssistantInput();

  await page.route('*/**/chat/assistants-management/new', async (route) => {
    if (route.request().method() === 'POST') {
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

  await createAssistant(page, assistantInput);

  await expect(page.getByText('Error creating assistant')).toBeVisible();
});

test('it can search for assistants', async ({ page }) => {
  const assistantInput1 = getFakeNewAssistantInput();
  const assistantInput2 = getFakeNewAssistantInput();

  await createAssistant(page, assistantInput1);
  await createAssistant(page, assistantInput2);

  // Search by name
  await page.waitForURL('/chat/assistants-management');
  await page.getByRole('searchbox').fill(assistantInput1.name);

  await expect(page.getByText(assistantInput2.name)).not.toBeVisible();
  await expect(page.getByText(assistantInput1.name)).toBeVisible();

  // search by description
  await page.getByRole('searchbox').clear();
  await page.getByRole('searchbox').fill(assistantInput2.description);

  await expect(page.getByText(assistantInput2.name)).toBeVisible();
  await expect(page.getByText(assistantInput1.name)).not.toBeVisible();

  // Search by instructions
  await page.getByRole('searchbox').fill(assistantInput1.instructions);

  await expect(page.getByText(assistantInput2.name)).not.toBeVisible();
  await expect(page.getByText(assistantInput1.name)).toBeVisible();

  // cleanup
  await deleteAssistantByName(assistantInput1.name);
  await deleteAssistantByName(assistantInput2.name);
});

test('it can navigate with breadcrumbs', async ({ page }) => {
  await page.goto('/chat/assistants-management');
  await page.getByRole('button', { name: 'New Assistant' }).click();
  await page.waitForURL('/chat/assistants-management/new');
  await page.getByRole('link', { name: 'Assistants Management' }).click();
  await page.waitForURL('/chat/assistants-management');
  await page.getByRole('link', { name: 'Chat' }).click();
  await page.waitForURL('/chat');
});

test('it validates input', async ({ page }) => {
  await page.goto('/chat/assistants-management/new');
  await page.getByLabel('name').fill('my assistant');
  const saveButton = page.getByRole('button', { name: 'Save' });

  await saveButton.click();

  await expect(page.getByText('This field is required. Please enter a tagline.')).toHaveCount(1);
  await expect(page.getByText('This field is required. Please enter instructions.')).toHaveCount(1);

  // Test client side validation - errors disappear live without have to click save
  await page.getByLabel('description').fill('my description');

  await page.getByPlaceholder("You'll act as...").fill('my instructions');
  await expect(page.getByText('This field is required. Please enter a tagline.')).toHaveCount(0);
  await expect(page.getByText('This field is required. Please enter instructions.')).toHaveCount(0);
});
