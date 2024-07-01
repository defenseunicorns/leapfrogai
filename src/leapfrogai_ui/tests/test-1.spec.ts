import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:4173/');
  await page.getByRole('button', { name: 'Log In with UDS SSO' }).click();
  await page.getByLabel('Username or email').fill('fakekeycloakuser@test.com!zu7bVAhaZakF2j*y6ih');
  await page.getByLabel('Username or email').press('ControlOrMeta+z');
  await page.getByLabel('Password').click();
  await page.getByLabel('Password').fill('!zu7bVAhaZakF2j*y6ih');
  await page.getByRole('button', { name: 'Log In' }).click();
  await page.getByLabel('Six digit code').fill('621715');
  await page.getByRole('button', { name: 'Log In' }).click();
  await page.getByTestId('settings header action button').click();
  await page.getByRole('link', { name: 'File Management' }).click();
  await page.getByRole('cell', { name: 'test.pdf' }).first().click();
  await page.getByText('Chat File Management File').click();
  await page.getByRole('row', { name: 'test.pdf 1 Jul' }).locator('label').click();
});