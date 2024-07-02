import { number, object, string } from 'yup';

export const newAPIKeySchema = object({
  name: string().required(),
  expiration: number().required()
})
  .noUnknown(true)
  .strict();
