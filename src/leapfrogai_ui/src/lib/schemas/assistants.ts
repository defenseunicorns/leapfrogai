import { mixed, number, object, ObjectSchema, string, ValidationError } from 'yup';
import type { AssistantInput, EditAssistantInput } from '$lib/types/assistants';
import {
  ASSISTANTS_DESCRIPTION_MAX_LENGTH,
  ASSISTANTS_INSTRUCTIONS_MAX_LENGTH,
  ASSISTANTS_NAME_MAX_LENGTH,
  AVATAR_FILE_SIZE_ERROR_TEXT,
  MAX_AVATAR_SIZE
} from '$lib/constants';

export const supabaseAssistantInputSchema: ObjectSchema<AssistantInput> = object({
  name: string()
    .max(ASSISTANTS_NAME_MAX_LENGTH)
    .required('This field is required. Please enter a name.'),
  description: string()
    .max(ASSISTANTS_DESCRIPTION_MAX_LENGTH)
    .required('This field is required. Please enter a tagline.'),
  instructions: string()
    .max(ASSISTANTS_INSTRUCTIONS_MAX_LENGTH)
    .required('This field is required. Please enter instructions.'),
  temperature: number().required('Required'),
  data_sources: string(),
  avatar: string(),
  avatarFile: mixed<File>()
    .nullable()
    .test('fileType', 'Please upload an image.', (value) => value == null || value instanceof File)
    .test('fileSize', AVATAR_FILE_SIZE_ERROR_TEXT, (value) => {
      if (value == null) {
        return true;
      }
      if (value.size > MAX_AVATAR_SIZE) {
        return new ValidationError(AVATAR_FILE_SIZE_ERROR_TEXT);
      }
      return true;
    })
    .test('type', 'Invalid file type, accepted types are: jpeg and png', (value) => {
      if (value == null) {
        return true;
      }
      if (value.type !== 'image/jpeg' && value.type !== 'image/jpg' && value.type !== 'image/png') {
        return new ValidationError('Invalid file type, accepted types are: jpeg and png');
      }
      return true;
    }), // additional validation for avatar and pictogram is handled in Modal component
  pictogram: string()
})
  .noUnknown(true)
  .strict();

export const editAssistantInputSchema: ObjectSchema<EditAssistantInput> =
  supabaseAssistantInputSchema.concat(object({ id: string().required() }));
