import { expect, test } from './fixtures';
import {
  getSimpleMathQuestion,
  deleteTestFilesWithApi,
  sendMessage,
  loadChatPage,
  uploadFile
} from './helpers';
import type { Page } from '@playwright/test';

const loadFileManagementPage = async (page: Page) => {
  await page.goto('/chat/file-management');
  await expect(page).toHaveTitle('LeapfrogAI - File Management');
};

test.beforeEach(async ({ page }) => {
  await loadFileManagementPage(page);

  // Delete all rows with filenames that start with "test" and end in .pdf
  const testPdfRows = await page.getByRole('row', { name: 'test.pdf' }).all();
  const testPdfForDeletionPdfRows = await page.getByRole('row', { name: 'test2.pdf' }).all();

  const testRows = [...testPdfRows, ...testPdfForDeletionPdfRows];

  for (const row of testRows) {
    await row.getByRole('checkbox').click();
  }
  if (testRows.length === 1) {
    await page.getByText('Delete').click();
  }

  await page.reload();
});

test('it can navigate to the last visited thread with breadcrumbs', async ({ page }) => {
  const newMessage = getSimpleMathQuestion();
  await page.goto('/chat');
  await sendMessage(page, newMessage);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(2);

  const urlParts = new URL(page.url()).pathname.split('/');
  const threadId = urlParts[urlParts.length - 1];

  await page.goto('/chat/file-management');
  await page.getByRole('link', { name: 'Chat' }).click();
  await page.waitForURL(`/chat/${threadId}`);
});

test('it can navigate to the file management page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByLabel('Settings').click();
  await page.getByText('File Management').click();

  await expect(page).toHaveTitle('LeapfrogAI - File Management');
});

test('it can upload a file', async ({ page }) => {
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

test('it can delete multiple files', async ({ page }) => {
  const filename = 'test2.pdf';

  await uploadFile(page, `${filename}`);
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible(); // wait for upload to finish
  await uploadFile(page, `${filename}`);
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible();

  const checkboxes = await page.getByRole('checkbox').all();
  await checkboxes[1].check();
  await checkboxes[2].check();
  await page.getByText('Delete').click();
  await expect(page.getByText('Files Deleted')).toBeVisible();
});

test('shows an error toast when there is an error deleting a file', async ({ page }) => {
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

  await uploadFile(page);

  await expect(page.getByText('test.pdf imported successfully')).toBeVisible();
  await expect(page.getByText('test.pdf imported successfully')).not.toBeVisible(); // wait for upload to finish

  await deleteTestFilesWithApi();
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
