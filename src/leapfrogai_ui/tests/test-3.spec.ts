import { test, expect } from '@playwright/test';

await page.getByPlaceholder('Assistant name').click();
await page.getByPlaceholder('Assistant name').fill('Assistant 1');
await page.getByPlaceholder('Here to help...').click();
await page.getByPlaceholder('Here to help...').fill('My Assistant');
await page.getByPlaceholder('You\'ll act as...').click();
await page.getByPlaceholder('You\'ll act as...').fill('A helpful assistant');
await page.locator('.mini-avatar-container').click();
await page.locator('div:nth-child(1082) > svg').click();
await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
await page.getByRole('button', { name: 'Save' }).click();
await page.getByPlaceholder('Search').click();
await page.goto('http://localhost:5173/chat/assistants-management');
await page.getByRole('button', { name: 'New assistant' }).click();
await page.locator('.mini-avatar-container').click();
await page.getByRole('button', { name: 'Close the modal' }).click();
});
