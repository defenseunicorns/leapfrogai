import { type Message as VercelAIMessage } from '@ai-sdk/svelte';
import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';
import { normalizeTimestamp } from '$helpers/chatHelpers';
import { getFakeOpenAIMessage } from '$testUtils/fakeData';
import type { LFMessage } from '$lib/types/messages';

describe('chat helpers', () => {
  describe('normalizeTimestamp', () => {
    it('should return the correct timestamp for Date object', () => {
      const message: VercelAIMessage = {
        id: '123',
        content: 'test',
        role: 'user',
        createdAt: new Date('2024-01-01T00:00:00Z')
      };
      const timestamp = normalizeTimestamp(message);
      expect(timestamp).toBe(new Date('2024-01-01T00:00:00Z').getTime());
    });

    it('should return the correct timestamp for date string', () => {
      const message: LFMessage = {
        ...getFakeOpenAIMessage({ thread_id: '123', content: 'test', role: 'user' }),
        created_at: '2024-01-01T00:00:00Z'
      };
      const timestamp = normalizeTimestamp(message);
      expect(timestamp).toBe(new Date('2024-01-01T00:00:00Z').getTime());
    });

    it('should return the correct timestamp for milliseconds number', () => {
      const timestampValue = 1672531200000;
      const message: LFMessage = {
        id: '123',
        content: 'test',
        role: 'user',
        createdAt: timestampValue
      };
      const timestamp = normalizeTimestamp(message);
      expect(timestamp).toBe(timestampValue);
    });

    it('should return the correct timestamp for seconds number', () => {
      const timestampValue = 1672531200;
      const message: OpenAIMessage = {
        ...getFakeOpenAIMessage({ thread_id: '123', content: 'test', role: 'user' }),
        created_at: timestampValue
      };
      const timestamp = normalizeTimestamp(message);
      expect(timestamp).toBe(timestampValue * 1000);
    });

    it('should default to a timestamp in milliseconds of right now for invalid or missing date value', () => {
      const message: LFMessage = {
        ...getFakeOpenAIMessage({ thread_id: '123', content: 'test', role: 'user' }),
        createdAt: null,
        created_at: null
      };
      // Occasionally the timestamps can be off by 1 millisecond and fail the tests, so we just check seconds here
      const timestamp = Math.floor(normalizeTimestamp(message) / 1000);
      expect(timestamp).toBe(Math.floor(new Date().getTime() / 1000));
    });
  });
});
