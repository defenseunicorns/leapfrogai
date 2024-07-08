import * as yup from 'yup';
import threadSchema from '$schemas/threadSchema';

// These do not test all possible combinations, they are just smoke tests
describe('threadSchema', () => {
  it('should validate a valid thread object', async () => {
    const validThread = {
      id: 'thread-id',
      created_at: 1628073600000,
      messages: [],
      metadata: { label: 'test', user_id: 'user-id' },
      object: 'thread',
      tool_resources: {
        code_interpreter: { file_ids: ['file-id-1', 'file-id-2'] },
        file_search: {
          vector_store_ids: ['vector-id-1'],
          vector_stores: [
            {
              file_ids: ['file-id-3'],
              created_at: 1628073600000,
              metadata: { key1: 'value1', key2: 'value2' }
            }
          ]
        }
      }
    };

    await expect(threadSchema.validate(validThread)).resolves.toBe(validThread);
  });

  it('should invalidate a thread object with missing required fields', async () => {
    const invalidThread = {
      // Missing id and created_at
      messages: [],
      metadata: { label: 'test', user_id: 'user-id' },
      object: 'thread',
      tool_resources: null
    };

    await expect(threadSchema.validate(invalidThread)).rejects.toThrow(yup.ValidationError);
  });

  it('should invalidate a thread object with invalid fields', async () => {
    // incorrect object type
    const invalidMetadataThread = {
      id: 'thread-id',
      created_at: 1628073600000,
      messages: [],
      metadata: { label: 'test', user_id: 'user-id' },
      object: 'thread.message',
      tool_resources: null
    };

    await expect(threadSchema.validate(invalidMetadataThread)).rejects.toThrow(yup.ValidationError);
  });
});
