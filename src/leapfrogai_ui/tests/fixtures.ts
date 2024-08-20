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

// When using keycloak, the cookie value is missing ending " and }}, so instead we parse
// out the token with this function
const extractAccessToken = (jsonString: string) => {
  const tokenKey = '"access_token":"';
  const startIndex = jsonString.indexOf(tokenKey);

  if (startIndex === -1) return null;

  const tokenValueStart = startIndex + tokenKey.length;
  const tokenValueEnd = jsonString.indexOf('"', tokenValueStart);
  return jsonString.substring(tokenValueStart, tokenValueEnd);
};

export const getToken = () => {
  const authData = JSON.parse(fs.readFileSync('playwright/.auth/user.json', 'utf-8'));
  let cookie: Cookie;

  cookie = authData.cookies.find(
    (cookie: Cookie) => cookie.name === 'sb-supabase-kong-auth-token.0'
  );

  if (!cookie)
    cookie = authData.cookies.find(
      (cookie: Cookie) => cookie.name === 'sb-supabase-kong-auth-token'
    );

  const cookieStripped = cookie.value.split('base64-')[1];
  const decodedValue = Buffer.from(cookieStripped, 'base64').toString('utf-8');
  return extractAccessToken(decodedValue);
};
export const getOpenAIClient = () => {
  const token = getToken();
  return new OpenAI({
    apiKey: process.env.OPENAI_API_KEY || token,
    baseURL: process.env.OPENAI_API_KEY
      ? `${process.env.LEAPFROGAI_API_BASE_URL}/v1`
      : `${process.env.LEAPFROGAI_API_BASE_URL}/openai/v1`
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
