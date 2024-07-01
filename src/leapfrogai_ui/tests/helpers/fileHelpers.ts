import OpenAI from 'openai';
import fs from 'node:fs';
import type { Page } from '@playwright/test';
import { PDFDocument } from 'pdf-lib';
import { expect } from '../fixtures';

export const uploadFileWithApi = async (fileName = 'test.pdf', openAIClient: OpenAI) => {
  const file = fs.createReadStream(`./tests/fixtures/${fileName}`);

  return openAIClient.files.create({
    file: file,
    purpose: 'assistants'
  });
};
export const deleteFileWithApi = async (id: string, openAIClient: OpenAI) => {
  return openAIClient.files.del(id);
};
export const createPDF = async (filename = `${new Date().toISOString()}-test.pdf`) => {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage();
  // Get the width and height of the page
  const { height } = page.getSize();

  const fontSize = 30;
  page.drawText('Ribbit!', {
    x: 50,
    y: height - 4 * fontSize,
    size: fontSize
  });

  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(`./tests/fixtures/${filename}`, pdfBytes);
};
export const deleteFixtureFile = (filename: string) => {
  if (fs.existsSync(`./tests/fixtures/${filename}`)) {
    fs.unlinkSync(`./tests/fixtures/${filename}`);
  }
};

// Deletes files created in the ./tests/fixtures directory
export const deleteAllGeneratedFixtureFiles = () => {
  fs.readdir('./tests/fixtures', (err, files) => {
    if (err) {
      return;
    } else {
      const testPdfFiles = files.filter((file) => file.endsWith('-test.pdf'));
      const testTextFiles = files.filter((file) => file.endsWith('-test.pdf'));
      testPdfFiles.forEach((file) => {
        deleteFixtureFile(file);
      });
      testTextFiles.forEach((file) => {
        deleteFixtureFile(file);
      });
    }
  });
};

export const uploadFile = async (page: Page, filename = 'test.pdf', btnName = 'upload') => {
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByRole('button', { name: btnName }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles(`./tests/fixtures/${filename}`);
};
export const getFileTableRow = async (page: Page, filename: string) => {
  const rows = page.locator('table tr');
  let targetRow;
  for (let i = 0; i < (await rows.count()); i++) {
    const row = rows.nth(i);
    const rowText = await row.textContent();
    if (rowText?.includes(filename)) {
      targetRow = row;
      break;
    }
  }
  return targetRow;
};
export const createTextFile = (filename: string, content = 'hop') => {
  fs.writeFileSync(`./tests/fixtures/${filename}`, content);
};
export const deleteTestFilesWithApi = async (openAIClient: OpenAI) => {
  const list = await openAIClient.files.list();
  const idsToDelete: string[] = [];
  for await (const file of list) {
    if (file.filename.startsWith('test')) {
      idsToDelete.push(file.id);
    }
  }

  const promises = [];
  for (const id of idsToDelete) {
    promises.push(openAIClient.files.del(id));
  }
  await Promise.all(promises);
};
export const loadFileManagementPage = async (page: Page) => {
  await page.goto('/chat/file-management');
  await expect(page).toHaveTitle('LeapfrogAI - File Management');
};
export const initiateDeletion = async (page: Page, fileNameText: string) => {
  const deleteBtn = page.getByRole('button', { name: 'delete' });

  await deleteBtn.click();
  await expect(page.getByText('Checking for any assistants affected by deletion...')).toBeVisible();
  await expect(page.getByText(`Are you sure you want to delete ${fileNameText}`)).toBeVisible();
};
export const confirmDeletion = async (page: Page) => {
  const deleteBtns = await page.getByRole('button', { name: 'delete' }).all();
  await deleteBtns[1].click();
};
