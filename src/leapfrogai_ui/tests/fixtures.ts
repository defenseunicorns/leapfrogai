import { test as base } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';
import fs from 'node:fs';
import OpenAI from 'openai';

type MyFixtures = {
  clearDbData: () => Promise<void>;
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

export const test = base.extend<MyFixtures>({
  // eslint-disable-next-line  no-empty-pattern
  clearDbData: async ({}, use) => {
    const clearDbData = async () => {
      const supabase = createClient(
        process.env.PUBLIC_SUPABASE_URL!,
        process.env.SERVICE_ROLE_KEY!
      );

      await supabase.storage.emptyBucket('assistant_avatars');
    };

    await use(clearDbData);
  },
  // eslint-disable-next-line  no-empty-pattern
  openAIClient: async ({}, use) => {
    const authData = JSON.parse(fs.readFileSync('playwright/.auth/user.json', 'utf-8'));
    const cookie = authData.cookies.find(
      (cookie: Cookie) => cookie.name === 'sb-supabase-kong-auth-token.0'
    );

    const decodedValue = decodeURIComponent(cookie.value);
    // The cookie value is missing ending " and }, so we append it
    const parsedValue = JSON.parse(`${decodedValue}"}`);

    const client = new OpenAI({
      apiKey: parsedValue.access_token,
      baseURL: process.env.LEAPFROGAI_API_BASE_URL
    });
    await use(client);
  }
});

export { expect, type Page } from '@playwright/test';
