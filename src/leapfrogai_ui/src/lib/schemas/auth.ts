import { object, string } from 'yup';

export const emailPasswordSchema = object({
  email: string().email().required(),
  password: string().required()
});
