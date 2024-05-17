import { object, ObjectSchema, string } from 'yup';
import { MAX_LABEL_SIZE } from '$lib/constants';
import { env } from '$env/dynamic/public';
import type { NewMessageInput } from '$lib/types/messages';

const contentInputSchema = string().max(Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT)).required();

export const messageInputSchema: ObjectSchema<NewMessageInput> = object({
  thread_id: string().required(),
  content: contentInputSchema,
  role: string<'user' | 'assistant'>().required(),
  assistantId: string().uuid().optional()
})
  .noUnknown(true)
  .strict();

export const uuidSchema = object({
  id: string().uuid().required()
})
  .noUnknown(true)
  .strict();

export const deleteMessageSchema = object({
  thread_id: string().required(),
  message_id: string().required()
});

const labelSchema = string().min(1).max(MAX_LABEL_SIZE).required();

export const newThreadInputSchema = object({
  label: labelSchema
})
  .noUnknown(true)
  .strict();

export const updateThreadLabelSchema = object({
  id: string().required(),
  label: labelSchema
})
  .noUnknown(true)
  .strict();
