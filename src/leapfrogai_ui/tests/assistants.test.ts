import { expect, test } from './fixtures';
import { createAssistant, deleteActiveThread, deleteAllAssistants, loadChatPage } from './helpers';
import { getFakeAssistantInput } from '../testUtils/fakeData';
import type { ActionResult } from '@sveltejs/kit';

test.afterEach(async () => {
  await deleteAllAssistants();
});

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
  const assistantInput = getFakeAssistantInput();

  await createAssistant(page, assistantInput);

  await page.waitForURL('/chat/assistants-management');
  await expect(page.getByText('Assistant Created')).toBeVisible();
  await expect(page.getByTestId(`assistant-tile-${assistantInput.name}`)).toBeVisible();
});

test('displays an error toast when there is an error creating an assistant and remains on the assistant page', async ({
  page
}) => {
  const assistantInput = getFakeAssistantInput();

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

  await expect(page.getByText('Error Creating Assistant')).toBeVisible();
});
test('displays an error toast when there is an error editing an assistant and remains on the assistant page', async ({
  page
}) => {
  const assistantInput1 = getFakeAssistantInput();
  const assistantInput2 = getFakeAssistantInput();

  await createAssistant(page, assistantInput1);

  await page
    .getByTestId(`assistant-tile-${assistantInput1.name}`)
    .getByTestId('overflow-menu')
    .click();
  await page.getByRole('menuitem', { name: 'Edit' }).click();

  await page.waitForURL('/chat/assistants-management/edit/**/*');

  const assistantId = page.url().substring(page.url().lastIndexOf('/') + 1);

  await page.route(`*/**/chat/assistants-management/edit/${assistantId}`, async (route) => {
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

  await page.getByLabel('name').fill(assistantInput2.name);

  // Wait for modal save button to disappear if avatar modal was open
  const saveButtons = page.getByRole('button', { name: 'Save' });
  await expect(saveButtons).toHaveCount(1);

  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText('Error Editing Assistant')).toBeVisible();

  await page.waitForURL(`/chat/assistants-management/edit/${assistantId}`);
});

test('it can search for assistants', async ({ page, browserName }) => {
  // this test is flaky on webkit, passes manual testing
  if (browserName !== 'webkit') {
    const assistantInput1 = getFakeAssistantInput();
    const assistantInput2 = getFakeAssistantInput();

    await createAssistant(page, assistantInput1);
    await createAssistant(page, assistantInput2);

    // Search by name
    await page.waitForURL('/chat/assistants-management');
    await page.getByRole('searchbox').fill(assistantInput1.name);

    await expect(page.getByTestId(`assistant-tile-${assistantInput2.name}`)).not.toBeVisible();
    await expect(page.getByTestId(`assistant-tile-${assistantInput1.name}`)).toBeVisible();

    // search by description
    await page.getByRole('searchbox').clear();
    await page.getByRole('searchbox').fill(assistantInput2.description);

    await expect(page.getByTestId(`assistant-tile-${assistantInput2.name}`)).toBeVisible();
    await expect(page.getByTestId(`assistant-tile-${assistantInput1.name}`)).not.toBeVisible();

    // Search by instructions
    await page.getByRole('searchbox').fill(assistantInput1.instructions);

    await expect(page.getByTestId(`assistant-tile-${assistantInput2.name}`)).not.toBeVisible();
    await expect(page.getByTestId(`assistant-tile-${assistantInput1.name}`)).toBeVisible();
  }
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

test('it confirms you want to navigate away if you have changes', async ({ page }) => {
  await page.goto('/chat/assistants-management/new');
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
  await page.goto('/chat/assistants-management/new');

  await page.getByRole('link', { name: 'Assistants Management' }).click();

  await page.waitForURL('/chat/assistants-management');
});

test('it DOES NOT confirm you want to navigate away if you click the cancel button', async ({
  page
}) => {
  await page.goto('/chat/assistants-management/new');
  await page.getByLabel('name').fill('my assistant');

  await page.getByRole('button', { name: 'Cancel' }).click();

  await page.waitForURL('/chat/assistants-management');
});

test('it allows you to edit an assistant', async ({ page }) => {
  const pictogramName = 'Analytics';
  const assistantInput1 = getFakeAssistantInput();
  const assistantInput2 = getFakeAssistantInput();

  await createAssistant(page, assistantInput1);

  await page.waitForURL('/chat/assistants-management');

  await page
    .getByTestId(`assistant-tile-${assistantInput1.name}`)
    .getByTestId('overflow-menu')
    .click();
  await page.getByRole('menuitem', { name: 'Edit' }).click();

  await page.getByLabel('name').fill(assistantInput2.name);
  await page.getByLabel('description').fill(assistantInput2.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput2.instructions);

  await page.locator('.mini-avatar-container').click();
  await page.getByTestId(`pictogram-${pictogramName}`).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  // Wait for modal save button to disappear if avatar modal was open
  const saveButtons = page.getByRole('button', { name: 'Save' });
  await expect(saveButtons).toHaveCount(1);

  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText('Assistant Updated')).toBeVisible();
  await expect(page.getByTestId(`assistant-tile-${assistantInput2.name}`)).toBeVisible();
});

test("it populates the assistants values when editing an assistant's details", async ({ page }) => {
  const assistantInput = getFakeAssistantInput();

  await createAssistant(page, assistantInput);

  await page.waitForURL('/chat/assistants-management');

  await page
    .getByTestId(`assistant-tile-${assistantInput.name}`)
    .getByTestId('overflow-menu')
    .click();
  await page.getByRole('menuitem', { name: 'Edit' }).click();

  await expect(page.getByLabel('name')).toHaveValue(assistantInput.name);
  await expect(page.getByLabel('description')).toHaveValue(assistantInput.description);
  await expect(page.getByPlaceholder("You'll act as...")).toHaveValue(assistantInput.instructions);
});

test('it can delete assistants', async ({ page }) => {
  const assistantInput = getFakeAssistantInput();

  await createAssistant(page, assistantInput);

  await page.goto('/chat/assistants-management');

  await page
    .getByTestId(`assistant-tile-${assistantInput.name}`)
    .getByTestId('overflow-menu')
    .click();

  // click overflow menu delete btn
  await page.getByRole('menuitem', { name: 'Delete' }).click();

  // click modal actual delete btn
  await page.getByRole('button', { name: 'Delete' }).click();

  await expect(page.getByText(`${assistantInput.name} Assistant deleted.`)).toBeVisible();
  await deleteActiveThread(page);
});
