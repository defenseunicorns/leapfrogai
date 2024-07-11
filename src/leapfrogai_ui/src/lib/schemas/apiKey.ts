import { number, object, type ObjectSchema, string } from 'yup';
import type { NewApiKeyInput } from '$lib/types/apiKeys';

export const newAPIKeySchema: ObjectSchema<NewApiKeyInput> = object({
  name: string(),
  expires_at: number().required()
})
  .noUnknown(true)
  .strict();
