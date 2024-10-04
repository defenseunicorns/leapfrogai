import { expect, test } from './fixtures';
import { getFakeAssistantInput } from '../testUtils/fakeData';
import { NO_FILE_ERROR_TEXT } from '../src/lib/constants/index';
import {
  createAssistantWithApi,
  deleteAllAssistants,
  deleteAssistantWithApi,
  editAssistantCard,
  fillOutRequiredAssistantFields,
  getRandomPictogramName,
  saveAssistant,
  saveAvatarImage,
  savePictogram,
  uploadAvatar
} from './helpers/assistantHelpers';
import { loadEditAssistantPage, loadNewAssistantPage } from './helpers/navigationHelpers';

test.afterEach(async ({ openAIClient }) => {
  await deleteAllAssistants(openAIClient);
});

test('it can search for and choose a pictogram as an avatar', async ({ page }) => {
  // We need each browser to pick a different pictogram
  // this can result in collisions and a flaky test
  // Attempts to import the iconMap and pick random pictograms failed, the import breaks this test file and it won't
  // show up in playwright
  const assistantInput = getFakeAssistantInput();
  const pictogramName = getRandomPictogramName();

  await loadNewAssistantPage(page);

  await fillOutRequiredAssistantFields(assistantInput, page);

  await page.getByTestId('mini-avatar-container').click();

  await page.getByPlaceholder('Search').click();
  await page.getByPlaceholder('Search').fill(pictogramName);

  await page.getByTestId(`pictogram-${pictogramName}`).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  // Wait for modal save button to disappear
  const saveButton = page.getByRole('button', { name: 'Save' });
  await expect(saveButton).toHaveCount(1);

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-${pictogramName}`);
  await expect(pictogram).toBeVisible();
  await saveAssistant(assistantInput.name, page);

  await expect(page.getByTestId(`pictogram-${pictogramName}`)).toBeVisible();
});

// Note - once photo is uploaded, playwright is changing the url for the file so we cannot test the name of the image
test('it can upload an image as an avatar', async ({ page }) => {
  const assistantInput = getFakeAssistantInput();

  await loadNewAssistantPage(page);

  await fillOutRequiredAssistantFields(assistantInput, page);

  await page.getByTestId('mini-avatar-container').click();
  await uploadAvatar(page);

  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  await saveAssistant(assistantInput.name, page);
  const card = page.getByTestId(`assistant-card-${assistantInput.name}`);
  const avatar = card.getByTestId('assistant-card-avatar');
  const avatarSrc = await avatar.getAttribute('src');

  expect(avatarSrc).toBeDefined();
});

test('it keeps the avatar when an assistant has been edited', async ({ page }) => {
  const assistantInput = getFakeAssistantInput();

  await loadNewAssistantPage(page);

  await fillOutRequiredAssistantFields(assistantInput, page);

  await page.getByTestId('mini-avatar-container').click();
  await uploadAvatar(page);

  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  await saveAssistant(assistantInput.name, page);
  const card = page.getByTestId(`assistant-card-${assistantInput.name}`);
  const avatar = card.getByTestId('assistant-card-avatar');
  const originalAvatarSrc = await avatar.getAttribute('src');

  expect(originalAvatarSrc).toBeDefined();

  await page.waitForURL('/chat/assistants-management');
  await expect(page.getByTestId(`assistant-card-${assistantInput.name}`)).toBeVisible();
  await editAssistantCard(assistantInput.name, page);
  await page.getByLabel('tagline').fill('new description');
  await saveAssistant(assistantInput.name, page);

  const avatarSrcAfterUpdate = await avatar.getAttribute('src');
  expect(avatarSrcAfterUpdate!.split('?v=')[0]).toEqual(originalAvatarSrc?.split('?v=')[0]);
});

test('it can change an image uploaded as an avatar', async ({ page }) => {
  await loadNewAssistantPage(page);

  await page.getByTestId('mini-avatar-container').click();
  await uploadAvatar(page);

  const avatarUploadContainer = page.getByTestId('image-upload-avatar');
  const originalImageSource = await avatarUploadContainer.getAttribute('src');

  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  await page.getByTestId('mini-avatar-container').click();

  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByText('Change', { exact: true }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('./tests/fixtures/frog.png');

  const newImageSource = await avatarUploadContainer.getAttribute('src');
  expect(originalImageSource).not.toEqual(newImageSource);
});

test('it shows an error when clicking save on the upload tab if no image is uploaded', async ({
  page
}) => {
  const assistantInput = getFakeAssistantInput();

  await loadNewAssistantPage(page);

  await fillOutRequiredAssistantFields(assistantInput, page);

  await page.getByTestId('mini-avatar-container').click();
  await page.getByTestId('upload-radio-btn').check();

  const saveButton = page.getByRole('button', { name: 'Save' }).nth(0);

  await saveButton.click();

  await expect(page.getByText(NO_FILE_ERROR_TEXT)).toBeVisible();
});

// Note - not testing too large file size validation because we would have to store a large file just for a test

test('it removes an uploaded image and keeps the original pictogram on save', async ({ page }) => {
  await loadNewAssistantPage(page);
  await page.getByTestId('mini-avatar-container').click();

  await uploadAvatar(page);

  await page.getByText('Remove').click();

  await expect(page.getByTestId('image-upload-avatar')).toHaveCount(0);

  await page.getByTestId('pictogram-radio-btn').check();

  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-default`);
  await expect(pictogram).toBeVisible();
});

test('it keeps the original pictogram on cancel after uploading an image but not saving it', async ({
  page
}) => {
  await loadNewAssistantPage(page);
  await page.getByTestId('mini-avatar-container').click();

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
  await loadNewAssistantPage(page);
  await page.getByTestId('mini-avatar-container').click();

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
  await loadNewAssistantPage(page);
  await page.getByTestId('mini-avatar-container').click();

  await page.getByPlaceholder('Search').click();
  await page.getByPlaceholder('Search').fill(pictogramName);

  await page.getByTestId(`pictogram-${pictogramName}`).click();

  await page.getByLabel('Close modal').click();

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-default`);
  await expect(pictogram).toBeVisible();
});

test('it saves the pictogram if the save button is clicked on the pictogram tab even if an image was uploaded', async ({
  page
}) => {
  const pictogramName = 'Analytics';

  await loadNewAssistantPage(page);
  await page.getByTestId('mini-avatar-container').click();

  await uploadAvatar(page);
  await page.getByTestId('pictogram-radio-btn').check();

  await page.getByTestId(`pictogram-${pictogramName}`).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

  const miniAvatarContainer = page.getByTestId('mini-avatar-container');
  const pictogram = miniAvatarContainer.getByTestId(`pictogram-${pictogramName}`);
  await expect(pictogram).toBeVisible();
});

test('it can upload an image, then change to a pictogram, then change to an image', async ({
  page
}) => {
  // There are lots of edge cases for the avatar/pictogram upload flow, this tests a couple of them
  const assistantInput = getFakeAssistantInput();
  const pictogramName = getRandomPictogramName();

  await loadNewAssistantPage(page);

  await fillOutRequiredAssistantFields(assistantInput, page);

  await saveAvatarImage(page);
  await savePictogram(pictogramName, page);
  await saveAvatarImage(page);

  // create assistant
  await saveAssistant(assistantInput.name, page);

  const card = page.getByTestId(`assistant-card-${assistantInput.name}`);
  const avatar = card.getByTestId('assistant-card-avatar');
  const avatarSrc = await avatar.getAttribute('src');

  expect(avatarSrc).toBeDefined();
});

test('it deletes the avatar image from storage when the avatar', async ({ page, openAIClient }) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadEditAssistantPage(assistant.id, page);
  await saveAvatarImage(page);
  const saveButton = page.getByRole('button', { name: 'Save' }).nth(0);
  await saveButton.click();

  const card = page.getByTestId(`assistant-card-${assistant.name}`);
  const avatar = card.getByTestId('assistant-card-avatar');
  const avatarSrc = await avatar.getAttribute('src');
  const res = await fetch(avatarSrc!);

  expect(res.status).toBe(200);
  const contentType = res.headers.get('content-type');
  expect(contentType).toMatch(/^image\//);

  await loadEditAssistantPage(assistant.id, page);
  await savePictogram(getRandomPictogramName(), page);
  await saveButton.click();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  const res2 = await fetch(avatarSrc!);
  const resJson = await res2.json();
  expect(resJson.statusCode).toEqual('404');

  //cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
});
