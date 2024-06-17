import OpenAI from 'openai';
import { env } from '$env/dynamic/private';

export const getOpenAiClient = (access_token?: string) =>
  new OpenAI({
    apiKey: env.OPENAI_API_KEY ? env.OPENAI_API_KEY : access_token,
    baseURL: env.LEAPFROGAI_API_BASE_URL
  });
