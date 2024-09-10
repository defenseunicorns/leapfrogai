import { expect, type Page } from '@playwright/test';
import { faker } from '@faker-js/faker';
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  process.env.PUBLIC_SUPABASE_URL!,
  process.env.SERVICE_ROLE_KEY!,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
);

export const SHORT_RESPONSE_PROMPT = 'respond with no more than one sentence';
export const LONG_RESPONSE_PROMPT = 'write me a long poem';

// These messages result in faster responses to avoid timeout issues
export const getSimpleMathQuestion = () => {
  const operations = [
    { operation: 'add', preposition: 'to' },
    { operation: 'subtract', preposition: 'from' },
    { operation: 'divide', preposition: 'by' },
    { operation: 'multiply', preposition: 'by' }
  ];
  const randomOperation = faker.helpers.arrayElement(operations);
  const randomNumber1 = faker.number.int({ min: 1, max: 1000 });
  const randomNumber2 = faker.number.int({ min: 1, max: 1000 });
  return `${randomOperation.operation} ${randomNumber1} ${randomOperation.preposition} ${randomNumber2}, ${SHORT_RESPONSE_PROMPT}`;
};

export const getTableRow = async (page: Page, textToSearchWith: string, tableTestId = '') => {
  if (tableTestId) {
    await expect(page.getByTestId(tableTestId).getByText(textToSearchWith)).toBeVisible();
  }
  const rows = page.locator('table tr');
  let targetRow;
  for (let i = 0; i < (await rows.count()); i++) {
    const row = rows.nth(i);
    const rowText = await row.textContent();
    if (rowText?.includes(textToSearchWith)) {
      targetRow = row;
      break;
    }
  }
  if (!targetRow) {
    throw new Error('error getting row');
  }
  return targetRow;
};

export const normalizeWhitespace = (str: string) => str.replace(/\s+/g, ' ').trim();
