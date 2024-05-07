import { array, number, object, ObjectSchema, string, mixed } from 'yup';
import { ASSISTANTS_INSTRUCTIONS_MAX_LENGTH, ASSISTANTS_NAME_MAX_LENGTH } from '$lib/constants';

export const supabaseAssistantInputSchema: ObjectSchema<NewAssistantInput> = object({
  name: string().max(ASSISTANTS_NAME_MAX_LENGTH).required('Required'),
  description: string().max(ASSISTANTS_NAME_MAX_LENGTH).required('Required'),
  instructions: string().max(ASSISTANTS_INSTRUCTIONS_MAX_LENGTH).required('Required'),
  temperature: number().required('Required'),
  data_sources: string(),
  avatar: mixed()
})
  .noUnknown(true)
  .strict();
