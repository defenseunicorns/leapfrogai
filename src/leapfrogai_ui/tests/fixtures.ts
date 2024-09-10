import { test as base } from '@playwright/test';
import OpenAI from 'openai';
import fs from 'node:fs';

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

// Gets an access token from cookie
export const getAccessToken = async () => {
  try {
    const authData = JSON.parse(
      fs.readFileSync(`${process.cwd()}/playwright/.auth/user.json`, 'utf-8')
    );
    const cookie = authData.cookies.find(
      (cookie: Cookie) =>
        cookie.name === 'sb-supabase-kong-auth-token' ||
        cookie.name === 'sb-supabase-kong-auth-token.0' ||
        cookie.name === 'sb-supabase-kong-auth-token.1'
    );
    const cookieStripped = cookie.value.replace('base64-', '');
    // Decode the base64 string
    const convertedCookie = Buffer.from(cookieStripped, 'base64').toString('utf-8');
    // When using Keycloak, the converted cookie may not be a valid JSON string, when only using Supabase, it is
    let parsedCookie;
    try {
      // Attempt to parse the JSON string as is
      parsedCookie = JSON.parse(convertedCookie);
    } catch (error) {
      // Attempt to parse the JSON string with added closing characters
      parsedCookie = JSON.parse(convertedCookie + '"}}');
    }
    return parsedCookie.access_token;
  } catch (e) {
    console.error('Error getting access token', e);
    return '';
  }
};

export const getOpenAIClient = async () => {
  const token = await getAccessToken();
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
    const client = await getOpenAIClient();
    await use(client);
  }
});

export { expect, type Page } from '@playwright/test';
