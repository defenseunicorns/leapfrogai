import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  // Recording...
await page.goto('http://localhost:5173/');
await page.getByRole('button', { name: 'Log In with UDS SSO' }).click();
await page.getByLabel('Username or email').click();
await page.getByLabel('Username or email').fill('fakekeycloakuser@test.com');
await page.getByLabel('Password').click();
await page.getByLabel('Password').fill('!zu7bVAhaZakF2j*y6ih');
await page.getByRole('button', { name: 'Log In' }).click();
await page.getByLabel('Six digit code').fill('345587');
await page.getByLabel('Six digit code').press('Enter');
await page.goto('http://localhost:5173/');
await page.getByRole('button', { name: 'Log In with UDS SSO' }).click();
await page.getByTestId('settings header action button').click();
await page.locator('div').filter({ hasText: 'Assistants Management' }).nth(3).click();
await page.getByRole('button', { name: 'New assistant' }).click();
await page.locator('.mini-avatar-container').click();
await page.getByText('Upload', { exact: true }).click();
await page.locator('label').filter({ hasText: 'Upload from computer' }).click();
await page.getByLabel('Upload from computer').setInputFiles('Doug.png');
await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
await page.goto('http://localhost:5173/chat/assistants-management/new');
await page.getByRole('button', { name: 'Save' }).click();});