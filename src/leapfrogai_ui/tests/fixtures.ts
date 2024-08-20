import { test as base } from '@playwright/test';
import OpenAI from 'openai';

type MyFixtures = {
  openAIClient: OpenAI;
};

export const getOpenAIClient = () => {
  return new OpenAI({
    apiKey: process.env.OPENAI_API_KEY || process.env.SERVICE_ROLE_KEY,
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
