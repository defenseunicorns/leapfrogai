import { expect, test } from './fixtures';
import { getFakeAssistantInput } from '../testUtils/fakeData';
import { delay } from 'msw';
import {
  createPDF,
  createTextFile,
  deleteAllGeneratedFixtureFiles,
  deleteFileByName,
  deleteFileWithApi,
  deleteFixtureFile,
  deleteTestFilesWithApi,
  uploadFile,
  uploadFileWithApi
} from './helpers/fileHelpers';
import { faker } from '@faker-js/faker';
import {
  createAssistantWithApi,
  deleteAssistantCard,
  deleteAssistantWithApi,
  editAssistantCard
} from './helpers/assistantHelpers';
import { getSimpleMathQuestion, loadChatPage } from './helpers/helpers';
import {
  deleteActiveThread,
  sendMessage,
  waitForResponseToComplete
} from './helpers/threadHelpers';

test.afterAll(() => {
  deleteAllGeneratedFixtureFiles(); // cleanup any files that were not deleted during tests (e.g. due to test failure)
});

test('can edit an assistant and attach files to it', async ({ page, openAIClient }) => {
  const filename1 = `${faker.word.noun()}-test.pdf`;
  const filename2 = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename1);
  await createPDF(filename2);

  const uploadedFile1 = await uploadFileWithApi(filename1, 'application/pdf', openAIClient);
  const uploadedFile2 = await uploadFileWithApi(filename2, 'application/pdf', openAIClient);
  const assistant = await createAssistantWithApi({ openAIClient });

  await page.goto(`/chat/assistants-management/edit/${assistant.id}`);

  await page.getByTestId('file-select-dropdown-btn').click();
  const fileSelectContainer = page.getByTestId('file-select-container');
  await fileSelectContainer.getByTestId(`${uploadedFile1.id}-checkbox`).check();
  await fileSelectContainer.getByTestId(`${uploadedFile2.id}-checkbox`).check();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  // Cleanup
  await deleteFileWithApi(uploadedFile1.id, openAIClient);
  await deleteFileWithApi(uploadedFile2.id, openAIClient);
  await deleteAssistantWithApi(assistant.id, openAIClient);
  deleteFixtureFile(filename1);
  deleteFixtureFile(filename2);
});

test('can create a new assistant and attach files to it', async ({ page, openAIClient }) => {
  const assistantInput = getFakeAssistantInput();
  const filename1 = `${faker.word.noun()}-test.pdf`;
  const filename2 = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename1);
  await createPDF(filename2);
  const uploadedFile1 = await uploadFileWithApi(filename1, 'application/pdf', openAIClient);
  const uploadedFile2 = await uploadFileWithApi(filename2, 'application/pdf', openAIClient);
  await page.goto(`/chat/assistants-management/new`);

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('tagline').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.getByTestId('file-select-dropdown-btn').click();
  const fileSelectContainer = page.getByTestId('file-select-container');
  await fileSelectContainer.getByTestId(`${uploadedFile1.id}-checkbox`).check();
  await fileSelectContainer.getByTestId(`${uploadedFile2.id}-checkbox`).check();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Created')).toBeVisible();

  // Cleanup
  expect(page.waitForURL('/chat/assistants-management'));
  await deleteAssistantCard(assistantInput.name, page);
  await deleteFileWithApi(uploadedFile1.id, openAIClient);
  await deleteFileWithApi(uploadedFile2.id, openAIClient);
  deleteFixtureFile(filename1);
  deleteFixtureFile(filename2);
});

test('it can edit an assistant and remove a file', async ({ page, openAIClient }) => {
  const filename1 = `${faker.word.noun()}-test.pdf`;
  const filename2 = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename1);
  await createPDF(filename2);
  const uploadedFile1 = await uploadFileWithApi(filename1, 'application/pdf', openAIClient);
  const uploadedFile2 = await uploadFileWithApi(filename2, 'application/pdf', openAIClient);
  const assistant = await createAssistantWithApi({ openAIClient });
  await page.goto(`/chat/assistants-management/edit/${assistant.id}`);

  // Create assistant with files
  await page.getByTestId('file-select-dropdown-btn').click();
  const fileSelectContainer = page.getByTestId('file-select-container');
  await fileSelectContainer.getByTestId(`${uploadedFile1.id}-checkbox`).check();
  await fileSelectContainer.getByTestId(`${uploadedFile2.id}-checkbox`).check();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  await editAssistantCard(assistant.name!, page);

  await page.waitForURL('/chat/assistants-management/edit/**/*');

  // Deselect
  await page.getByTestId('file-select-dropdown-btn').click();
  await fileSelectContainer.getByTestId(`${uploadedFile1.id}-checkbox`).uncheck();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  // Cleanup
  await deleteFileWithApi(uploadedFile1.id, openAIClient);
  await deleteFileWithApi(uploadedFile2.id, openAIClient);
  await deleteAssistantWithApi(assistant.id, openAIClient);
  deleteFixtureFile(filename1);
  deleteFixtureFile(filename2);
});

test('while creating an assistant, it can upload new files and save the assistant', async ({
  page,
  openAIClient
}) => {
  const assistantInput = getFakeAssistantInput();
  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  await page.goto('/chat/assistants-management/new');

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('tagline').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.getByTestId('file-select-dropdown-btn').click();
  await uploadFile(page, filename, 'Upload new data source');

  const saveBtn = await page.getByRole('button', { name: 'Save' });
  expect(saveBtn).toBeDisabled();
  await expect(saveBtn).not.toBeDisabled();

  await saveBtn.click();
  await expect(page.getByText(`${filename} imported successfully.`)).toBeVisible();
  await expect(page.getByText('Assistant Created')).toBeVisible();

  // Cleanup
  expect(page.waitForURL('/chat/assistants-management'));
  await deleteAssistantCard(assistantInput.name, page);
  await deleteTestFilesWithApi(openAIClient);
  deleteFixtureFile(filename);
  await deleteFileByName(filename, openAIClient);
});

test('while editing an assistant, it can upload new files and save the assistant', async ({
  page,
  openAIClient
}) => {
  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  const assistant = await createAssistantWithApi({ openAIClient });
  await page.goto(`/chat/assistants-management/edit/${assistant.id}`);

  await page.getByTestId('file-select-dropdown-btn').click();
  await uploadFile(page, filename, 'Upload new data source');

  const saveBtn = await page.getByRole('button', { name: 'Save' });
  expect(saveBtn).toBeDisabled();
  await expect(saveBtn).not.toBeDisabled();

  await saveBtn.click();
  await expect(page.getByText(`${filename} imported successfully.`)).toBeVisible();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  // Cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
  await deleteTestFilesWithApi(openAIClient);
  await deleteFileByName(filename, openAIClient);
  deleteFixtureFile(filename);
});

test('it displays a failed toast and temporarily failed uploader item when a the file upload endpoint completely fails', async ({
  page,
  openAIClient
}) => {
  // Mock a complete backend failure
  await page.route('*/**/chat/file-management', async (route) => {
    await route.abort('failed');
  });

  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  await page.goto('/chat/assistants-management/new');

  await page.getByTestId('file-select-dropdown-btn').click();
  await uploadFile(page, filename, 'Upload new data source');

  await expect(page.getByText(`Upload Failed`)).toBeVisible();
  await expect(page.getByTestId(`${filename}-error-uploader-item`)).toBeVisible();
  await delay(1500);
  await expect(page.getByTestId(`${filename}-error-uploader-item`)).not.toBeVisible();

  // Cleanup
  deleteFixtureFile(filename);
  await deleteFileByName(filename, openAIClient);
});

test('it displays an uploading indicator temporarily when uploading a file', async ({
  page,
  openAIClient
}) => {
  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  await page.goto('/chat/assistants-management/new');

  await page.getByTestId('file-select-dropdown-btn').click();
  await uploadFile(page, filename, 'Upload new data source');

  await expect(page.getByTestId(`${filename}-uploading-uploader-item`)).toBeVisible();
  await expect(page.getByTestId(`${filename}-uploading-uploader-item`)).not.toBeVisible();

  // Cleanup
  deleteFixtureFile(filename);
  await deleteFileByName(filename, openAIClient);
});

// Note - have been unable to test open in new tab btn, only testing download button
test('can download a file from the citation', async ({ page, openAIClient }) => {
  const filename = await createPDF();
  const uploadedFile = await uploadFileWithApi(filename, 'application/pdf', openAIClient);
  const fakeAssistantInput = getFakeAssistantInput([uploadedFile.id]);
  const assistant = await createAssistantWithApi({
    assistantInput: fakeAssistantInput,
    openAIClient
  });
  const newMessage = getSimpleMathQuestion();
  await loadChatPage(page);
  const messages = page.getByTestId('message');

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant.name!).click();
  await sendMessage(page, newMessage);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  await page.getByTestId(`${uploadedFile.id}-citation-btn`).click();
  await expect(page.getByTitle(`${uploadedFile.id}-iframe`)).toBeVisible();

  const downloadPromise = page.waitForEvent('download');
  await page.getByTestId('file-download-btn').click();
  const download = await downloadPromise;

  expect(download.suggestedFilename()).toEqual(filename.replace(/:/g, '_'));

  // cleanup
  await deleteActiveThread(page, openAIClient);
  await deleteFileWithApi(uploadedFile.id, openAIClient);
  await deleteAssistantWithApi(assistant.id, openAIClient);
});

test('it shows a spinner then opens an iframe when a pdf citation is clicked on', async ({
  page,
  openAIClient
}) => {
  const filename = await createPDF();
  const uploadedFile = await uploadFileWithApi(filename, 'application/pdf', openAIClient);
  const fakeAssistantInput = getFakeAssistantInput([uploadedFile.id]);
  const assistant = await createAssistantWithApi({
    assistantInput: fakeAssistantInput,
    openAIClient
  });

  await loadChatPage(page);

  const newMessage = getSimpleMathQuestion();
  await loadChatPage(page);
  const messages = page.getByTestId('message');

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant.name!).click();
  await sendMessage(page, newMessage);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  await page.getByTestId(`${uploadedFile.id}-citation-btn`).click();
  await expect(page.getByTestId('file-processing-spinner')).toBeVisible();
  await expect(page.getByTitle(`${uploadedFile.id}-iframe`)).toBeVisible();
  await expect(page.getByTestId('file-processing-spinner')).not.toBeVisible();
  // iFrame content is not showing in Playwright, so we are not testing that the pdf contents are displayed

  // cleanup
  await deleteActiveThread(page, openAIClient);
  await deleteFileWithApi(uploadedFile.id, openAIClient);
  await deleteAssistantWithApi(assistant.id, openAIClient);
});

test('it shows a spinner then opens an iframe when a non-pdf citation is clicked on', async ({
  page,
  openAIClient
}) => {
  const filename = createTextFile();
  const uploadedFile = await uploadFileWithApi(filename, 'text/plain', openAIClient);
  const fakeAssistantInput = getFakeAssistantInput([uploadedFile.id]);
  const assistant = await createAssistantWithApi({
    assistantInput: fakeAssistantInput,
    openAIClient
  });

  await loadChatPage(page);

  const newMessage = getSimpleMathQuestion();
  await loadChatPage(page);
  const messages = page.getByTestId('message');

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant.name!).click();
  await sendMessage(page, newMessage);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  await page.getByTestId(`${uploadedFile.id}-citation-btn`).click();
  await expect(page.getByTestId('file-processing-spinner')).toBeVisible();
  await expect(page.getByTitle(`${uploadedFile.id}-iframe`)).toBeVisible();
  await expect(page.getByTestId('file-processing-spinner')).not.toBeVisible();
  // iframe content is not showing in Playwright, so we are not testing that the pdf contents are displayed

  // cleanup
  await deleteActiveThread(page, openAIClient);
  await deleteFileWithApi(uploadedFile.id, openAIClient);
  await deleteAssistantWithApi(assistant.id, openAIClient);
});
