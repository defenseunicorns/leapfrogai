import OpenAI from 'openai';
import { env } from '$env/dynamic/private';

export const openai = new OpenAI({
  apiKey: env.LEAPFROGAI_API_KEY ?? '',
  baseURL: env.LEAPFROGAI_API_BASE_URL
});
