import { type Message as AIMessage } from 'ai/svelte';
import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';
import { normalizeTimestamp, sortMessages } from '$helpers/chatHelpers';
import { getFakeOpenAIMessage } from '$testUtils/fakeData';
import type { LFMessage } from '$lib/types/messages';

describe('chat helpers', () => {
  describe('normalizeTimestamp', () => {
    it('should return the correct timestamp for Date object', () => {
      const message: AIMessage = {
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

    it('should return 0 for invalid or missing date value', () => {
      const message: LFMessage = {
        ...getFakeOpenAIMessage({ thread_id: '123', content: 'test', role: 'user' }),
        createdAt: null,
        created_at: null
      };
      const timestamp = normalizeTimestamp(message);
      expect(timestamp).toBe(0);
    });
  });

  describe('sortMessages', () => {
    it('should sort messages by timestamp in ascending order', () => {
      const messages: Array<AIMessage | OpenAIMessage> = [
        { id: '1', content: 'test1', role: 'user', createdAt: new Date('2024-01-01T00:00:00Z') },
        { id: '2', content: 'test2', role: 'user', createdAt: new Date('2024-01-02T00:00:00Z') },
        { id: '3', content: 'test3', role: 'user', createdAt: new Date('2024-01-03T00:00:00Z') }
      ];

      const sortedMessages = sortMessages(messages);

      expect(sortedMessages[0].id).toBe('1');
      expect(sortedMessages[1].id).toBe('2');
      expect(sortedMessages[2].id).toBe('3');
    });
  });
});
