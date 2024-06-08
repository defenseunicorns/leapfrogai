import { expect, test } from './fixtures';
import { loadChatPage } from './helpers';
import type { Page } from '@playwright/test';

const loadFileManagementPage = async (page: Page) => {
  await page.goto('/chat/file-management');
  await expect(page).toHaveTitle('LeapfrogAI - File Management');
};

const uploadFile = async (page: Page, filename = 'test.pdf') => {
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByRole('button', { name: /upload/i }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles(`./tests/fixtures/${filename}`);
};

const deleteFile = async (page: Page) => {
  const checkboxes = await page.getByRole('checkbox').all();
  await checkboxes[1].check(); // first checkbox is for selecting all, pick the second one
  await page.getByText('Delete').click();
};

test.beforeEach(async ({ page }) => {
  console.log('After Each running');
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

  console.log('After Each completed');
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

  await deleteFile(page);
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
