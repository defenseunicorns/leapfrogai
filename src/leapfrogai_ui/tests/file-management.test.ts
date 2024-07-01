import { expect, test } from './fixtures';
import { faker } from '@faker-js/faker';
import { getSimpleMathQuestion, loadChatPage, sendMessage } from './helpers';
import {
  confirmDeletion,
  createPDF,
  createTextFile,
  deleteAllGeneratedFixtureFiles,
  deleteFixtureFile,
  deleteTestFilesWithApi,
  getFileTableRow,
  initiateDeletion,
  loadFileManagementPage,
  uploadFile
} from './helpers/fileHelpers';

test.beforeEach(async ({ openAIClient }) => {
  await deleteTestFilesWithApi(openAIClient);
});

test.afterAll(() => {
  deleteAllGeneratedFixtureFiles(); // cleanup any files that were not deleted during tests (e.g. due to test failure)
});

test('it can navigate to the last visited thread with breadcrumbs', async ({ page }) => {
  const newMessage = getSimpleMathQuestion();
  await page.goto('/chat');
  await sendMessage(page, newMessage);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(2);

  const urlParts = new URL(page.url()).pathname.split('/');
  const threadId = urlParts[urlParts.length - 1];

  await page.getByLabel('Settings').click();
  await page.getByText('File Management').click();
  await page.getByRole('link', { name: 'Chat' }).click();
  await page.waitForURL(`/chat/${threadId}`);
});

test('it can navigate to the file management page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByLabel('Settings').click();
  await page.getByText('File Management').click();

  await expect(page).toHaveTitle('LeapfrogAI - File Management');
});

test('it can upload a pdf file', async ({ page }) => {
  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);
  await loadFileManagementPage(page);
  await uploadFile(page, filename);

  const row = await getFileTableRow(page, filename);
  expect(row).not.toBeNull();

  const uploadingFileIcon = row!.getByTestId('uploading-file-icon');
  const fileUploadedIcon = row!.getByTestId('file-uploaded-icon');

  // test loading icon shows then disappears
  await expect(uploadingFileIcon).toBeVisible();
  // Ensure an additional checkbox is not added during upload (it should not have one on that row. row is in nonSelectableRowIds)
  const rowCheckboxesBefore = await row!.getByRole('checkbox').all();
  expect(rowCheckboxesBefore.length).toEqual(0);
  await expect(fileUploadedIcon).toBeVisible();
  await expect(uploadingFileIcon).not.toBeVisible();

  // Checkbox should now be present
  const rowCheckboxesAfter = await row!.getByRole('checkbox').all();
  expect(rowCheckboxesAfter.length).toEqual(1);

  // test toast
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();

  // test complete icon disappears
  await expect(fileUploadedIcon).not.toBeVisible();

  // cleanup
  deleteFixtureFile(filename);
  row!.getByRole('checkbox').check({ force: true });
  await initiateDeletion(page, filename);
  await confirmDeletion(page);
});

test('it can upload a txt file', async ({ page }) => {
  const filename = `${faker.word.noun()}-test.txt`;
  createTextFile(filename);
  await loadFileManagementPage(page);
  await uploadFile(page, filename);

  const row = await getFileTableRow(page, filename);
  expect(row).not.toBeNull();

  const uploadingFileIcon = row!.getByTestId('uploading-file-icon');
  const fileUploadedIcon = row!.getByTestId('file-uploaded-icon');

  // test loading icon shows then disappears
  await expect(uploadingFileIcon).toBeVisible();
  // Ensure an additional checkbox is not added during upload (it should not have one on that row. row is in nonSelectableRowIds)
  const rowCheckboxesBefore = await row!.getByRole('checkbox').all();
  expect(rowCheckboxesBefore.length).toEqual(0);
  await expect(fileUploadedIcon).toBeVisible();
  await expect(uploadingFileIcon).not.toBeVisible();

  // Checkbox should now be present
  const rowCheckboxesAfter = await row!.getByRole('checkbox').all();
  expect(rowCheckboxesAfter.length).toEqual(1);

  // test toast
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();

  // test complete icon disappears
  await expect(fileUploadedIcon).not.toBeVisible();

  // cleanup
  deleteFixtureFile(filename);
  row!.getByRole('checkbox').check({ force: true });
  await initiateDeletion(page, filename);
  await confirmDeletion(page);
});

test('confirms any affected assistants then deletes multiple files', async ({ page }) => {
  await loadFileManagementPage(page);

  const filename1 = `${faker.word.noun()}-test.pdf`;
  const filename2 = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename1);
  await createPDF(filename2);

  await uploadFile(page, filename1);
  await expect(page.getByText(`${filename1} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename1} imported successfully`)).not.toBeVisible(); // wait for upload to finish
  await uploadFile(page, `${filename2}`);
  await expect(page.getByText(`${filename2} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename2} imported successfully`)).not.toBeVisible();

  const row1 = await getFileTableRow(page, filename1);
  const row2 = await getFileTableRow(page, filename2);
  expect(row1).not.toBeNull();
  expect(row2).not.toBeNull();

  await row1!.getByRole('checkbox').check({ force: true });
  await row2!.getByRole('checkbox').check({ force: true });
  await initiateDeletion(page, `${filename1}, ${filename2}`);
  await confirmDeletion(page);

  await expect(page.getByText('Files Deleted')).toBeVisible();

  // cleanup
  deleteFixtureFile(filename1);
  deleteFixtureFile(filename2);
});

test('it cancels the delete confirmation modal', async ({ page }) => {
  await loadFileManagementPage(page);

  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  await uploadFile(page, filename);
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible(); // wait for upload to finish

  const row = await getFileTableRow(page, filename);
  expect(row).not.toBeNull();
  await row!.getByRole('checkbox').check({ force: true });

  await initiateDeletion(page, filename);

  const cancelBtn = page.getByRole('dialog').getByRole('button', { name: 'Cancel' });
  await cancelBtn.click();
  await expect(page.getByText(`Are you sure you want to delete ${filename}`)).not.toBeVisible();

  // Cleanup
  deleteFixtureFile(filename);
  await initiateDeletion(page, filename);
  await confirmDeletion(page);
});

// TODO - this test doesn't clean up created files b/c we need to un-mock the error then cleanup
test('shows an error toast when there is an error deleting a file', async ({ page }) => {
  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  let hasBeenCalled = false;
  await page.route('*/**/api/files/delete', async (route) => {
    if (!hasBeenCalled && route.request().method() === 'DELETE') {
      if (!hasBeenCalled && route.request().method() === 'DELETE') {
        hasBeenCalled = true;
        await route.fulfill({ status: 500 });
      } else {
        const response = await route.fetch();
        await route.fulfill({ response });
      }
    }
  });
  await loadFileManagementPage(page);
  await uploadFile(page, filename);

  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible(); // wait for upload to finish

  const row = await getFileTableRow(page, filename);
  expect(row).not.toBeNull();
  await row!.getByRole('checkbox').check({ force: true });

  await initiateDeletion(page, filename);
  await confirmDeletion(page);

  await expect(page.getByText('Error Deleting File')).toBeVisible();

  // Cleanup
  deleteFixtureFile(filename);
});

test('it shows toast when there is an error submitting the form', async ({ page, browserName }) => {
  // Test passes on all browsers individually, but fails randomly when run in parallel. Unknown why.
  // Not a critical test, so only running on Firefox.
  if (browserName === 'firefox') {
    await page.route('*/**/chat/file-management', async (route) => {
      if (route.request().method() === 'POST') {
        const json = {};

        await route.fulfill({ json });
      } else {
        const response = await route.fetch();
        await route.fulfill({ response });
      }
    });

    await loadFileManagementPage(page);

    const filename = `${faker.word.noun()}-test.pdf`;
    await createPDF(filename);

    await uploadFile(page, filename);

    await expect(page.getByText('Import Failed')).toBeVisible();

    // Cleanup
    deleteFixtureFile(filename);
  }
});
