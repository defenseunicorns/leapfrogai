import * as yup from 'yup';
import { array, object, string } from 'yup';

const fileCitationAnnotationSchema = yup.object().shape({
  end_index: yup.number().required(),
  file_citation: yup
    .object()
    .shape({
      file_id: yup.string().required(),
      quote: yup.string().required()
    })
    .required(),
  start_index: yup.number().required(),
  text: yup.string().required(),
  type: yup.mixed().oneOf(['file_citation']).required()
});

const filePathAnnotationSchema = yup.object().shape({
  end_index: yup.number().required(),
  file_path: yup
    .object()
    .shape({
      file_id: yup.string().required()
    })
    .required(),
  start_index: yup.number().required(),
  text: yup.string().required(),
  type: yup.mixed().oneOf(['file_path']).required()
});

const annotationSchema = yup.lazy((value) => {
  if (value.type === 'file_citation') {
    return fileCitationAnnotationSchema;
  }
  if (value.type === 'file_path') {
    return filePathAnnotationSchema;
  }
  return yup.mixed().oneOf(['file_citation', 'file_path']).required(); // This will catch invalid types
});

const imageFileSchema = yup.object().shape({
  file_id: yup.string().required(),
  detail: yup.mixed().oneOf(['auto', 'low', 'high'])
});

const imageFileContentBlockSchema = yup.object().shape({
  image_file: imageFileSchema.required(),
  type: yup.mixed().oneOf(['image_file']).required()
});

const imageUrlSchema = yup.object().shape({
  url: yup.string().url().required(),
  detail: yup.mixed().oneOf(['auto', 'low', 'high'])
});

const imageUrlContentBlockSchema = yup.object().shape({
  image_url: imageUrlSchema.required(),
  type: yup.mixed().oneOf(['image_url']).required()
});

const textSchema = yup.object().shape({
  annotations: yup.array().of(annotationSchema).required(),
  value: yup.string().required()
});

const textContentBlockSchema = yup.object().shape({
  text: textSchema.required(),
  type: yup.mixed().oneOf(['text']).required()
});

const messageSchema = yup
  .object()
  .shape({
    id: yup.string().required(),
    assistant_id: yup.string().nullable(),
    attachments: yup
      .array()
      .of(
        yup.object().shape({
          file_id: yup.string(),
          tools: yup.array().of(yup.mixed().oneOf(['code_interpreter', 'file_search']))
        })
      )
      .nullable(),
    completed_at: yup.number().nullable(),
    content: yup
      .array()
      .of(
        yup.lazy((value) => {
          if (value.type === 'text') {
            return textContentBlockSchema;
          }
          if (value.type === 'image_file') {
            return imageFileContentBlockSchema;
          }
          if (value.type === 'image_url') {
            return imageUrlContentBlockSchema;
          }
          return yup.mixed().oneOf(['text', 'image_file', 'image_url']).required();
        })
      )
      .required(),
    created_at: yup.number().required(),
    incomplete_at: yup.number().nullable(),
    incomplete_details: yup
      .object()
      .shape({
        reason: yup
          .mixed()
          .oneOf(['content_filter', 'max_tokens', 'run_cancelled', 'run_expired', 'run_failed'])
      })
      .nullable(),
    metadata: object({ user_id: string() }).test(
      'max fields',
      'metadata is limited to 16 fields',
      (value) => Object.keys(value).length <= 16
    ),
    object: yup.mixed().oneOf(['thread.message']).required(),
    role: yup.mixed().oneOf(['user', 'assistant']).required(),
    run_id: yup.string().nullable(),
    status: yup.mixed().oneOf(['in_progress', 'incomplete', 'completed']), // openai type has this as required, but it's not being returned on message creation
    thread_id: yup.string().required()
  })
  .noUnknown(true)
  .strict();

export const AIMessagesInputSchema = yup
  .object({
    messages: array().of(
      object({ role: string<'user' | 'assistant'>().required(), content: string().required() })
        .noUnknown(true)
        .strict()
    )
  })
  .noUnknown(true)
  .strict();

export default messageSchema;
