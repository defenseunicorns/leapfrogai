import { number, object, string } from 'yup';

export const newAPIKeySchema = object({
  name: string().required(),
  expires_at: number().required()
})
  .noUnknown(true)
  .strict();
