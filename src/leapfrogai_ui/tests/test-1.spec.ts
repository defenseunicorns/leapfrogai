import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.getByPlaceholder('You\'ll act as...').fill('asd');
  await page.getByPlaceholder('Assistant name').click();
  await page.getByPlaceholder('Assistant name').fill('asd');
  await page.getByPlaceholder('Here to help...').click();
  await page.getByPlaceholder('Here to help...').fill('asd');
  await page.getByPlaceholder('You\'ll act as...').click();
  await page.getByPlaceholder('You\'ll act as...').fill('sd');
  await page.getByRole('button', { name: 'Save' }).click();
  await page.locator('[id="ccs-0\\.nicq3ikpq8d"]').click();
  await page.getByRole('menuitem', { name: 'Edit' }).click();
  await page.getByPlaceholder('Assistant name').click();
  await page.getByPlaceholder('Assistant name').fill('asd123');
  await page.getByPlaceholder('Here to help...').click();
  await page.getByPlaceholder('Here to help...').fill('asdasd');
  await page.getByPlaceholder('You\'ll act as...').fill('asda');
  await page.getByPlaceholder('You\'ll act as...').click();
  await page.getByPlaceholder('You\'ll act as...').fill('asdasd');
  await page.locator('.bx--slider').click();
  await page.getByTestId('mini-avatar-container').click();
  await page.locator('[id="bx--modal-body--ccs-0\\.nu0tsig62m"] div').filter({ hasText: 'Pictogram Upload' }).nth(1).click();
  await page.locator('button:nth-child(26)').click();
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
  await page.getByRole('button', { name: 'Save' }).click();
  await page.goto('http://localhost:5173/chat/assistants-management');
  await page.getByTestId('overflow-menu').click();
  await page.getByRole('menuitem', { name: 'Delete' }).click();
  await page.getByRole('button', { name: 'Delete' }).click();

  await page.goto('http://localhost:5173/chat/assistants-management');}