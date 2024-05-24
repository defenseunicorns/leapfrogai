import * as yup from 'yup';
import { array, object, string } from 'yup';
import messageSchema from '$schemas/messageSchema';

export const threadImportSchema = array().of(
  object({
    label: string()
  })
);

const threadToolResourcesSchema = yup.object().shape({
  code_interpreter: yup.object().shape({
    file_ids: yup.array().of(yup.string())
  }),
  file_search: yup.object().shape({
    vector_store_ids: yup.array().of(yup.string()),
    vector_stores: yup.array().of(
      yup.object().shape({
        file_ids: yup.array().of(yup.string()),
        created_at: yup.number().required(),
        metadata: object().test(
          'max fields',
          'metadata is limited to 16 fields',
          (value) => Object.keys(value).length <= 16
        )
      })
    )
  })
});

const threadSchema = yup
  .object()
  .shape({
    id: yup.string().required(),
    created_at: yup.number().required(),
    messages: yup.array().of(messageSchema),
    metadata: object({ label: string(), user_id: string() }).test(
      'max fields',
      'metadata is limited to 16 fields',
      (value) => Object.keys(value).length <= 16
    ),
    object: yup.mixed().oneOf(['thread']).required(),
    tool_resources: threadToolResourcesSchema.nullable()
  })
  .noUnknown(true)
  .strict();

export const threadsSchema = array().of(threadSchema);

export default threadSchema;
