import { expect, test } from './fixtures';
import {
  deleteTestFilesWithApi,
  getSimpleMathQuestion,
  loadChatPage,
  sendMessage,
  uploadFile
} from './helpers';
import type { Page } from '@playwright/test';

const loadFileManagementPage = async (page: Page) => {
  await page.goto('/chat/file-management');
  await expect(page).toHaveTitle('LeapfrogAI - File Management');
};

const initiateDeletion = async (page: Page, fileNameText: string) => {
  const deleteBtn = page.getByRole('button', { name: 'delete' });

  await deleteBtn.click();
  await expect(page.getByText('Checking for any assistants affected by deletion...')).toBeVisible();
  await expect(page.getByText(`Are you sure you want to delete ${fileNameText}`)).toBeVisible();
};
const confirmDeletion = async (page: Page) => {
  const deleteBtns = await page.getByRole('button', { name: 'delete' }).all();
  await deleteBtns[1].click();
};

// TODO - these tests are flaky because they use the same two files (test.pdf and test2.pdf) and there can
// be race conditions when uploading and deleting them while tests run in parallel

test.beforeEach(async ({ openAIClient }) => {
  await deleteTestFilesWithApi(openAIClient);
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
  await loadFileManagementPage(page);
  const checkboxes = await page.getByRole('checkbox').all();
  await uploadFile(page);
  const checkboxesDuringUpload = await page.getByRole('checkbox').all();

  // test loading icon shows then disappears
  await expect(page.getByTestId('uploading-file-icon')).toBeVisible();
  // Ensure an additional checkbox is not added during upload (it should not have one on that row. row is in nonSelectableRowIds)
  await expect(checkboxesDuringUpload.length).toEqual(checkboxes.length);
  await expect(page.getByTestId('uploading-file-icon')).not.toBeVisible();

  const checkboxesAfterUpload = await page.getByRole('checkbox').all();
  // Checkbox should now be present
  await expect(checkboxesAfterUpload.length).toEqual(checkboxes.length + 1);

  // test toast
  await expect(page.getByText('test.pdf imported successfully')).toBeVisible();

  // test complete icon shows then disappears
  await expect(page.getByTestId('file-uploaded-icon')).toBeVisible();
  await expect(page.getByTestId('file-uploaded-icon')).not.toBeVisible();
});

test('it can upload a txt file', async ({ page }) => {
  const checkboxes = await page.getByRole('checkbox').all();
  await uploadFile(page, 'test.txt');
  const checkboxesDuringUpload = await page.getByRole('checkbox').all();

  // test loading icon shows then disappears
  await expect(page.getByTestId('uploading-file-icon')).toBeVisible();
  // Ensure an additional checkbox is not added during upload (it should not have one on that row. row is in nonSelectableRowIds)
  await expect(checkboxesDuringUpload.length).toEqual(checkboxes.length);
  await expect(page.getByTestId('uploading-file-icon')).not.toBeVisible();

  const checkboxesAfterUpload = await page.getByRole('checkbox').all();
  // Checkbox should now be present
  await expect(checkboxesAfterUpload.length).toEqual(checkboxes.length + 1);

  // test toast
  await expect(page.getByText('test.txt imported successfully')).toBeVisible();

  // test complete icon shows then disappears
  await expect(page.getByTestId('file-uploaded-icon')).toBeVisible();
  await expect(page.getByTestId('file-uploaded-icon')).not.toBeVisible();
});

test('confirms any affected assistants then deletes multiple files', async ({ page }) => {
  await loadFileManagementPage(page);

  const filename1 = 'test.pdf';
  const filename2 = 'test2.pdf';

  await uploadFile(page, filename1);
  await expect(page.getByText(`${filename1} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename1} imported successfully`)).not.toBeVisible(); // wait for upload to finish
  await uploadFile(page, `${filename2}`);
  await expect(page.getByText(`${filename2} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename2} imported successfully`)).not.toBeVisible();

  const checkboxes = await page.getByRole('checkbox').all();
  await checkboxes[1].check({ force: true });
  await checkboxes[2].check({ force: true });
  await initiateDeletion(page, '');
  await confirmDeletion(page);

  await expect(page.getByText('Files Deleted')).toBeVisible();
});

test('it cancel the delete confirmation modal', async ({ page }) => {
  await loadFileManagementPage(page);

  const filename = 'test.pdf';

  await uploadFile(page, filename);
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible(); // wait for upload to finish

  const checkboxes = await page.getByRole('checkbox').all();
  await checkboxes[1].check({ force: true });

  await initiateDeletion(page, filename);

  const cancelBtn = page.getByRole('dialog').getByRole('button', { name: 'Cancel' });
  await cancelBtn.click();
  await expect(page.getByText(`Are you sure you want to delete ${filename}`)).not.toBeVisible();
});

test('shows an error toast when there is an error deleting a file', async ({ page }) => {
  const filename = 'test.pdf';
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

  await expect(page.getByText('test.pdf imported successfully')).toBeVisible();
  await expect(page.getByText('test.pdf imported successfully')).not.toBeVisible(); // wait for upload to finish

  const checkboxes = await page.getByRole('checkbox').all();
  await checkboxes[1].check({ force: true });

  await initiateDeletion(page, filename);
  await confirmDeletion(page);

  await expect(page.getByText('Error Deleting File')).toBeVisible();
});

test('it shows toast when there is an error submitting the form', async ({ page }) => {
  await page.route('*/**/chat/file-management', async (route) => {
    if (route.request().method() === 'POST') {
      const json = {};

      await route.fulfill({ json });
    } else {
      const response = await route.fetch();
      await route.fulfill({ response });
    }
  });

  await uploadFile(page);
  await expect(page.getByText('Import Failed')).toBeVisible();
});
