import { expect, test } from './fixtures';
import { getFakeAssistantInput } from '../testUtils/fakeData';
import { deleteAssistant, uploadAvatar } from './helpers';
import { NO_FILE_ERROR_TEXT } from '../src/lib/constants/index';

test('it can search for and choose a pictogram as an avatar', async ({ page }) => {
  const assistantInput = getFakeAssistantInput();

  const pictogramName = 'Analytics';

  await page.goto('/chat/assistants-management/new');

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('description').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.locator('.mini-avatar-container').click();

  await page.getByPlaceholder('Search').click();
  await page.getByPlaceholder('Search').fill(pictogramName);

  await page.getByTestId(`pictogram-${pictogramName}`).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  // Wait for modal save button to disappear
  const saveButtons = page.getByRole('button', { name: 'Save' });
  await expect(saveButtons).toHaveCount(1);

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-${pictogramName}`);
  await expect(pictogram).toBeVisible();

  // cleanup
  await deleteAssistant(page, assistantInput.name);
});

// Note - once photo is uploaded, playwright is changing the url for the file so we cannot test the name of the image
test('it can upload an image as an avatar', async ({ page }) => {
  const assistantInput = getFakeAssistantInput();

  await page.goto('/chat/assistants-management/new');

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('description').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.locator('.mini-avatar-container').click();
  await uploadAvatar(page);

  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  // Wait for modal save button to disappear
  const saveButtons = page.getByRole('button', { name: 'Save' });
  await expect(saveButtons).toHaveCount(1);

  await saveButtons.click();

  await page.waitForURL('/chat/assistants-management');
  await expect(page.getByText('Assistant Created')).toBeVisible();
  await expect(page.getByTestId(`assistant-tile-${assistantInput.name}`)).toBeVisible();

  // cleanup
  await deleteAssistant(page, assistantInput.name);
});

test('it can change an image uploaded as an avatar', async ({ page }) => {
  await page.goto('/chat/assistants-management/new');

  await page.locator('.mini-avatar-container').click();
  await uploadAvatar(page);

  const imageUploadContainer = page.getByTestId('image-upload-avatar');
  const backgroundImage = await imageUploadContainer.evaluate((node) => {
    return window.getComputedStyle(node).backgroundImage;
  });

  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  await page.locator('.mini-avatar-container').click();

  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByText('Change', { exact: true }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('./tests/fixtures/frog.png');

  const newBackgroundImage = await imageUploadContainer.evaluate((node) => {
    return window.getComputedStyle(node).backgroundImage;
  });

  expect(backgroundImage).not.toEqual(newBackgroundImage);
});

test('it shows an error when clicking save on the upload tab if no image is uploaded', async ({
  page
}) => {
  const assistantInput = getFakeAssistantInput();

  await page.goto('/chat/assistants-management/new');

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('description').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.locator('.mini-avatar-container').click();
  await page.getByText('Upload', { exact: true }).click();

  const saveButton = page.getByRole('button', { name: 'Save' }).nth(0);

  await saveButton.click();

  await expect(page.getByText(NO_FILE_ERROR_TEXT)).toBeVisible();
});

// Note - not testing too large file size validation because we would have to store a large file just for a test

test('it removes an uploaded image and keeps the original pictogram on save', async ({ page }) => {
  await page.goto('/chat/assistants-management/new');
  await page.locator('.mini-avatar-container').click();

  await uploadAvatar(page);

  await page.getByText('Remove').click();

  await expect(page.getByTestId('image-upload-avatar')).toHaveCount(0);

  await page.getByText('Pictogram', { exact: true }).click();

  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-default`);
  await expect(pictogram).toBeVisible();
});

test('it keeps the original pictogram on cancel after uploading an image but not saving it', async ({
  page
}) => {
  await page.goto('/chat/assistants-management/new');
  await page.locator('.mini-avatar-container').click();

  await uploadAvatar(page);

  await page.getByText('Cancel').nth(0).click();

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-default`);
  await expect(pictogram).toBeVisible();
});

test('it keeps the original pictogram on cancel after changing the pictogram but not saving it', async ({
  page
}) => {
  const pictogramName = 'Analytics';
  await page.goto('/chat/assistants-management/new');
  await page.locator('.mini-avatar-container').click();

  await page.getByPlaceholder('Search').click();
  await page.getByPlaceholder('Search').fill(pictogramName);

  await page.getByTestId(`pictogram-${pictogramName}`).click();

  await page.getByText('Cancel').nth(0).click();

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-default`);
  await expect(pictogram).toBeVisible();
});

// Testing close button, not cancel button. Close and Cancel should remain connected to the same helper function so only testing one edge case
test('it keeps the original pictogram on close (not cancel) after changing the pictogram but not saving it', async ({
  page
}) => {
  const pictogramName = 'Analytics';
  await page.goto('/chat/assistants-management/new');
  await page.locator('.mini-avatar-container').click();

  await page.getByPlaceholder('Search').click();
  await page.getByPlaceholder('Search').fill(pictogramName);

  await page.getByTestId(`pictogram-${pictogramName}`).click();

  await page.getByLabel('Close the modal').nth(0).click();

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-default`);
  await expect(pictogram).toBeVisible();
});

test('it saves the pictogram if the save button is clicked on the pictogram tab even if an image was uploaded', async ({
  page
}) => {
  const pictogramName = 'Analytics';

  await page.goto('/chat/assistants-management/new');
  await page.locator('.mini-avatar-container').click();

  await uploadAvatar(page);

  await page.getByText('Pictogram', { exact: true }).click();

  await page.getByTestId(`pictogram-${pictogramName}`).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-${pictogramName}`);
  await expect(pictogram).toBeVisible();
});
