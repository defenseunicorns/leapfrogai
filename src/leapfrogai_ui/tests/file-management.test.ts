import { expect, test } from './fixtures';
import { loadChatPage } from './helpers';
import type { Page } from '@playwright/test';

const loadFileManagementPage = async (page: Page) => {
  await page.goto('/chat/file-management');
  await expect(page).toHaveTitle('LeapfrogAI - File Management');
};

const uploadFile = async (page: Page) => {
  await page.getByText('Upload').click();

  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByText('Upload').click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('./tests/fixtures/test.pdf');
};

const deleteFile = async (page: Page) => {
  await page.getByTestId('file-management-settings').click();
  await page.getByRole('menuitem', { name: 'Edit' }).click();
  const checkboxes = await page.getByRole('checkbox').all();
  await checkboxes[1].check(); // first checkbox is for selecting all, pick the second one
  await page.getByText('Delete').click();
};

test('it can navigate to the file management page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByLabel('Settings').click();
  await page.getByText('File Management').click();

  await expect(page).toHaveTitle('LeapfrogAI - File Management');
});

test('it can upload a file', async ({ page }) => {
  await loadFileManagementPage(page);
  await uploadFile(page);
  await expect(page.getByText('test.pdf imported successfully')).toBeVisible();

  // Cleanup
  await deleteFile(page);
  await expect(page.getByText('File deleted')).toBeVisible();
});

test('it can delete multiple files', async ({ page }) => {
  await loadFileManagementPage(page);
  await uploadFile(page);
  await expect(page.getByText('test.pdf imported successfully')).toBeVisible();
  await expect(page.getByText('test.pdf imported successfully')).not.toBeVisible(); // wait for upload to finish
  await uploadFile(page);
  await expect(page.getByText('test.pdf imported successfully')).toBeVisible();
  await expect(page.getByText('test.pdf imported successfully')).not.toBeVisible();

  await page.getByTestId('file-management-settings').click();
  await page.getByRole('menuitem', { name: 'Edit' }).click();
  const checkboxes = await page.getByRole('checkbox').all();
  await checkboxes[1].check();
  await checkboxes[2].check();
  await page.getByText('Delete').click();
  await expect(page.getByText('Files deleted')).toBeVisible();
});

test('shows an error toast when there is an error deleting a file', async ({ page }) => {
  let hasBeenCalled = false;
  await page.route('*/**/api/files/delete', async (route) => {
    if (!hasBeenCalled && route.request().method() === 'DELETE') {
      hasBeenCalled = true;
      await route.fulfill({ status: 500 });
    } else {
      const response = await route.fetch();
      await route.fulfill({ response });
    }
  });

  await loadFileManagementPage(page);
  await uploadFile(page);
  await expect(page.getByText('test.pdf imported successfully')).toBeVisible();
  await expect(page.getByText('test.pdf imported successfully')).not.toBeVisible(); // wait for upload to finish

  await deleteFile(page);
  await expect(page.getByText('Error Deleting Files')).toBeVisible();
  const existingFile = await page.getByText('test.pdf').all();
  expect(existingFile).toHaveLength(1);

  // Cleanup
  await page.getByText('Cancel').click(); // close toolbar so deleteFile helper will work
  await deleteFile(page);
  await expect(page.getByText('File deleted')).toBeVisible();
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
  await loadFileManagementPage(page);
  await uploadFile(page);
  await expect(page.getByText('Import Failed')).toBeVisible();
});
