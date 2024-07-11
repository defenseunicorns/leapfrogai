import { test as base } from '@playwright/test';
import fs from 'node:fs';
import OpenAI from 'openai';

type MyFixtures = {
  openAIClient: OpenAI;
};

type Cookie = {
  name: string;
  value: string;
  domain: string;
  path: string;
  expires: number;
  httpOnly: boolean;
  secure: boolean;
  sameSite: string;
};

export const getToken = () => {
  const authData = JSON.parse(fs.readFileSync('playwright/.auth/user.json', 'utf-8'));
  const cookie = authData.cookies.find(
    (cookie: Cookie) => cookie.name === 'sb-supabase-kong-auth-token.0'
  );

  const decodedValue = decodeURIComponent(cookie.value);
  // The cookie value is missing ending " and }, so we append it
  const parsedValue = JSON.parse(`${decodedValue}"}`);
  return parsedValue.access_token;
};
export const getOpenAIClient = () => {
  const token = getToken();
  return new OpenAI({
    apiKey: process.env.OPENAI_API_KEY || token,
    baseURL: `${process.env.LEAPFROGAI_API_BASE_URL}/openai/v1`
  });
};

export const test = base.extend<MyFixtures>({
  // eslint-disable-next-line  no-empty-pattern
  openAIClient: async ({}, use) => {
    const client = getOpenAIClient();
    await use(client);
  }
});

export { expect, type Page } from '@playwright/test';
