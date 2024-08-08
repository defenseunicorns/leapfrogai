import OpenAI from 'openai';
import fs from 'node:fs';
import type { Page } from '@playwright/test';
import { PDFDocument } from 'pdf-lib';
import XLSX from 'xlsx';
import { Document, Packer, Paragraph } from 'docx';
import pptxgen from 'pptxgenjs';
import { expect } from '../fixtures';
import type { FileObject } from 'openai/resources/files';
import { getTableRow } from './helpers';

export const uploadFileWithApi = async (
  filename = 'test.pdf',
  contentType = 'application/pdf',
  openAIClient: OpenAI
) => {
  const filePath = `./tests/fixtures/${filename}`;
  const fileContent = fs.readFileSync(filePath);

  const file = new File([new Blob([fileContent])], filename, {
    type: contentType
  });

  // This can also be done IAW the OpenAI API documentation with fs.createReadStream, but Leapfrog API does not currently
  // support a ReadStream. Open Issue: https://github.com/defenseunicorns/leapfrogai/issues/710

  return openAIClient.files.create({
    file,
    purpose: 'assistants'
  });
};
export const deleteFileWithApi = async (id: string, openAIClient: OpenAI) => {
  return openAIClient.files.del(id);
};

/* ------ FILE CREATORS ------ */
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
  return filename;
};

type CreateFileOptions = {
  filename?: string;
  extension?: string;
};

export const createTextFile = (options: CreateFileOptions = {}) => {
  const { filename = `${new Date().toISOString()}-test`, extension = '.txt' } = options;
  const filenameWithExtension = `${filename}${extension}`;
  const content = 'hop';
  fs.writeFileSync(`./tests/fixtures/${filenameWithExtension}`, content);
  return filenameWithExtension;
};

export const createWordFile = (options: CreateFileOptions = {}) => {
  const { filename = `${new Date().toISOString()}-test`, extension = '.docx' } = options;
  const filenameWithExtension = `${filename}${extension}`;
  const doc = new Document({
    sections: [{ children: [new Paragraph({ text: 'LeapfrogAI' })] }]
  });
  Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync(`./tests/fixtures/${filenameWithExtension}`, buffer);
  });
  return filenameWithExtension;
};

export const createExcelFile = (options: CreateFileOptions = {}) => {
  const { filename = `${new Date().toISOString()}-test`, extension = '.xlsx' } = options;
  const filenameWithExtension = `${filename}${extension}`;

  const workbook = XLSX.utils.book_new();
  const worksheet = XLSX.utils.json_to_sheet([{ Name: 'Leapfrog', Age: 1, Type: 'AI' }]);
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
  XLSX.writeFile(workbook, `./tests/fixtures/${filenameWithExtension}`);

  return filenameWithExtension;
};

export const createPowerpointFile = async (options: { filename?: string } = {}) => {
  const { filename = `${new Date().toISOString()}-test` } = options;

  const presentation = new pptxgen();
  const slide = presentation.addSlide();
  const textboxText = 'Hello from LeapfrogAI';
  const textboxOpts = { x: 1, y: 1, color: '363636' };
  slide.addText(textboxText, textboxOpts);
  await presentation.writeFile({ fileName: `./tests/fixtures/${filename}` });

  return `${filename}.pptx`;
};

/* ------ END FILE CREATORS ------ */

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
      const testPdfFiles = files.filter((file) => file.includes('test'));
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

export const deleteFileByName = async (filename: string, openAIClient: OpenAI) => {
  const list = await openAIClient.files.list();

  for await (const file of list) {
    if (file.filename === filename) {
      openAIClient.files.del(file.id);
    }
  }
};

export const deleteAllTestFilesWithApi = async (openAIClient: OpenAI) => {
  try {
    const list = await openAIClient.files.list();
    const files = list.data as FileObject[];

    for (const file of files) {
      if (file.filename.includes('test')) {
        openAIClient.files.del(file.id);
      }
    }
  } catch (e) {
    console.error(`Error deleting test files`, e);
  }
};

export const testFileUpload = async (filename: string, page: Page, openAIClient: OpenAI) => {
  await loadFileManagementPage(page);
  await uploadFile(page, filename);

  const row = await getTableRow(page, filename, 'file-management-table');
  expect(row).not.toBeNull();

  const uploadingFileIcon = row!.getByTestId('uploading-file-spinner');
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
  await deleteFileByName(filename, openAIClient);
};
