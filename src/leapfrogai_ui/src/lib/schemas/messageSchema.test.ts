import messageSchema from '$schemas/messageSchema';
import type { LFMessage } from '$lib/types/messages';
import { ValidationError } from 'yup';

// These do not test all possible combinations, they are just smoke tests
describe('Message Schema', () => {
  it('should validate a valid message object', async () => {
    const validMessage: LFMessage = {
      id: 'msg_123',
      assistant_id: null,
      attachments: null,
      completed_at: null,
      content: [
        {
          text: {
            annotations: [
              {
                end_index: 10,
                file_citation: {
                  file_id: 'file_123',
                  quote: 'example quote'
                },
                start_index: 0,
                text: 'example text',
                type: 'file_citation'
              }
            ],
            value: 'This is an example message.'
          },
          type: 'text'
        }
      ],
      created_at: 1625077335,
      incomplete_at: null,
      incomplete_details: null,
      metadata: {
        user_id: 'user_123'
      },
      object: 'thread.message',
      role: 'user',
      run_id: null,
      status: 'completed',
      thread_id: 'thread_123'
    };

    await expect(messageSchema.validate(validMessage)).resolves.toBe(validMessage);
  });

  it('should invalidate a message with invalid fields', async () => {
    // incorrect type in annotation
    const invalidMessage = {
      id: 'msg_123',
      assistant_id: null,
      attachments: null,
      completed_at: null,
      content: [
        {
          text: {
            annotations: [
              {
                end_index: 10,
                file_citation: {
                  file_id: 'file_123',
                  quote: 'example quote'
                },
                start_index: 0,
                text: 'example text',
                type: 'invalid_type' // Invalid type
              }
            ],
            value: 'This is an example message.'
          },
          type: 'text'
        }
      ],
      created_at: 1625077335,
      incomplete_at: null,
      incomplete_details: null,
      metadata: {},
      object: 'thread.message',
      role: 'user',
      run_id: null,
      status: 'completed',
      thread_id: 'thread_123'
    };

    await expect(messageSchema.validate(invalidMessage)).rejects.toThrow(ValidationError);
  });

  it('should invalidate a message with missing required fields', async () => {
    // Missing 'id' field
    const invalidMessage = {
      assistant_id: null,
      attachments: null,
      completed_at: null,
      content: [
        {
          text: {
            annotations: [
              {
                end_index: 10,
                file_citation: {
                  file_id: 'file_123',
                  quote: 'example quote'
                },
                start_index: 0,
                text: 'example text',
                type: 'file_citation'
              }
            ],
            value: 'This is an example message.'
          },
          type: 'text'
        }
      ],
      created_at: 1625077335,
      incomplete_at: null,
      incomplete_details: null,
      metadata: {},
      object: 'thread.message',
      role: 'user',
      run_id: null,
      status: 'completed',
      thread_id: 'thread_123'
    };

    await expect(messageSchema.validate(invalidMessage)).rejects.toThrow(ValidationError);
  });
});
