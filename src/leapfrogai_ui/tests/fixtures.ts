import { test as base } from '@playwright/test';
import OpenAI from 'openai';

type MyFixtures = {
  openAIClient: OpenAI;
};

export async function getAccessToken() {
  const supabaseUrl = process.env.PUBLIC_SUPABASE_URL;
  const serviceRoleKey = process.env.SERVICE_ROLE_KEY;

  // Typically, the access token generation would be for something like an auth login,
  // but since you mentioned using the service role key, you'd perform operations directly.

  const response = await fetch(`${supabaseUrl}/auth/v1/token?grant_type=password`, {
    method: 'POST',
    // @ts-expect-error: apikey is a required header for this request
    headers: {
      'Content-Type': 'application/json',
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`
    },
    body: JSON.stringify({
      email: process.env.USERNAME,
      password: process.env.PASSWORD
    })
  });

  const data = await response.json();

  if (response.ok) {
    console.log('Access Token:', data.access_token);
    return data.access_token;
  } else {
    console.error('Error fetching access token:', data);
    throw new Error(data.error_description || 'Failed to fetch access token');
  }
}

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
    console.log('client', client);
    await use(client);
  }
});

export { expect, type Page } from '@playwright/test';
