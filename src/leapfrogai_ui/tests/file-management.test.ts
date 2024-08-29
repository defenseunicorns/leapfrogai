import { expect, test } from './fixtures';
import { getTableRow, getSimpleMathQuestion } from './helpers/helpers';
import {
  confirmDeletion,
  createCSVFile,
  createExcelFile,
  createPDF,
  createPowerpointFile,
  createTextFile,
  createWordFile,
  deleteAllGeneratedFixtureFiles,
  deleteFileByName,
  deleteFixtureFile,
  deleteTestFilesWithApi,
  initiateDeletion,
  testFileUpload,
  uploadFile
} from './helpers/fileHelpers';
import { sendMessage } from './helpers/threadHelpers';
import {
  loadFileManagementPage,
  navigateToChatPage,
  navigateToFileManagementPage
} from './helpers/navigationHelpers';

test.beforeEach(async ({ page, openAIClient }) => {
  await deleteTestFilesWithApi(openAIClient);
  await loadFileManagementPage(page);
});

test.afterEach(async ({ openAIClient }) => {
  deleteAllGeneratedFixtureFiles();
  await deleteTestFilesWithApi(openAIClient);
});

test('it can navigate to the last visited thread with breadcrumbs', async ({ page }) => {
  await navigateToChatPage(page);
  const newMessage = getSimpleMathQuestion();
  await sendMessage(page, newMessage);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(2);

  const urlParts = new URL(page.url()).pathname.split('/');
  const threadId = urlParts[urlParts.length - 1];

  await navigateToFileManagementPage(page);
  await page.getByTestId('breadcrumbs').getByRole('link', { name: 'Chat' }).click();
  await page.waitForURL(`/chat/${threadId}`);
});

test('it can navigate to the file management page', async ({ page }) => {
  await expect(page).toHaveTitle('LeapfrogAI - File Management');
});

test('it can upload a pdf file', async ({ page, openAIClient }) => {
  const filename = await createPDF();
  await testFileUpload(filename, page, openAIClient);
});

test('it can upload a .txt file', async ({ page, openAIClient }) => {
  const filename = createTextFile();
  await testFileUpload(filename, page, openAIClient);
});

test('it can upload a .text file', async ({ page, openAIClient }) => {
  const filename = createTextFile({ extension: '.text' });
  await testFileUpload(filename, page, openAIClient);
});

test('it can upload a .docx word file', async ({ page, openAIClient }) => {
  const filename = createWordFile();
  await testFileUpload(filename, page, openAIClient);
});

test('it can upload a .doc word file', async ({ page, openAIClient }) => {
  const filename = createWordFile({ extension: '.doc' });
  await testFileUpload(filename, page, openAIClient);
});

test('it can upload a .xlsx excel file', async ({ page, openAIClient }) => {
  const filename = createExcelFile();
  await testFileUpload(filename, page, openAIClient);
});

test('it can upload a .xls excel file', async ({ page, openAIClient }) => {
  const filename = createExcelFile({ extension: '.xls' });
  await testFileUpload(filename, page, openAIClient);
});

test('it can upload a .csv file', async ({ page, openAIClient }) => {
  const filename = createCSVFile();
  await testFileUpload(filename, page, openAIClient);
});

// pptxgenjs library not capable of creating .ppt files, so only testing .pptx
test('it can upload a .pptx powerpoint file', async ({ page, openAIClient }) => {
  const filename = await createPowerpointFile();
  await testFileUpload(filename, page, openAIClient);
});

test('confirms any affected assistants then deletes multiple files', async ({ page }) => {
  const filename1 = await createPDF();
  const filename2 = await createPDF();

  await uploadFile(page, filename1);
  await expect(page.getByText(`${filename1} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename1} imported successfully`)).not.toBeVisible(); // wait for upload to finish
  await uploadFile(page, `${filename2}`);
  await expect(page.getByText(`${filename2} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename2} imported successfully`)).not.toBeVisible();

  const row1 = await getTableRow(page, filename1, 'file-management-table');
  const row2 = await getTableRow(page, filename2, 'file-management-table');
  expect(row1).not.toBeNull();
  expect(row2).not.toBeNull();

  await row1!.getByRole('checkbox').check({ force: true });
  await row2!.getByRole('checkbox').check({ force: true });
  await initiateDeletion(page, `${filename1}, ${filename2}`);
  await confirmDeletion(page);

  await expect(page.getByText('Files Deleted')).toBeVisible();
});

test('it cancels the delete confirmation modal', async ({ page, openAIClient }) => {
  const filename = await createPDF();

  await uploadFile(page, filename);
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible(); // wait for upload to finish

  const row = await getTableRow(page, filename, 'file-management-table');
  await row.getByRole('checkbox').check();

  await initiateDeletion(page, filename);

  const cancelBtn = page.getByRole('dialog').getByRole('button', { name: 'Cancel' });
  await cancelBtn.click();
  await expect(page.getByText(`Are you sure you want to delete ${filename}`)).not.toBeVisible();

  // Cleanup
  deleteFixtureFile(filename);
  await deleteFileByName(filename, openAIClient);
});

test('shows an error toast when there is an error deleting a file', async ({ page }) => {
  const filename = await createPDF();
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
  await uploadFile(page, filename);

  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible(); // wait for upload to finish

  const row = await getTableRow(page, filename, 'file-management-table');
  await row.getByRole('checkbox').check();

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

  const filename = await createPDF();

  await uploadFile(page, filename);

  await expect(page.getByText('Import Failed')).toBeVisible();
});

test('it can download a file', async ({ page }) => {
  const filename = await createPDF();

  await uploadFile(page, filename);
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible(); // wait for upload to finish

  const row = await getTableRow(page, filename, 'file-management-table');
  await row.getByRole('checkbox').check();

  const downloadPromise = page.waitForEvent('download');
  const downloadBtn = page.getByRole('button', { name: 'Download' });
  await downloadBtn.click();
  const download = await downloadPromise;

  expect(download.suggestedFilename()).toEqual(filename.replace(/:/g, '_'));
  await expect(page.getByText('File Downloaded')).toBeVisible();
  await expect(downloadBtn).not.toBeVisible(); // all items deselected
});

test('it notifies the user when a file has uploaded successfully, even when leaving the page', async ({
  page
}) => {
  const filename = await createPDF();
  await uploadFile(page, filename);
  await page.getByTestId('breadcrumbs').getByRole('link', { name: 'Chat' }).click();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).toBeVisible();
  await expect(page.getByText(`${filename} imported successfully`)).not.toBeVisible();
  await navigateToFileManagementPage(page);
  await expect(page.getByText(filename)).toBeVisible(); // ensure the file was still loaded into the list despite navigation
});
