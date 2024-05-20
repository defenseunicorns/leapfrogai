import type { Message, MessageContent } from 'openai/resources/beta/threads/messages';

export type NewMessageInput = {
  thread_id: string;
  content: string;
  role: 'user' | 'assistant';
  assistantId?: string;
};

export type LFMessage = Message & {
  content: string | MessageContent[];
  metadata: {
    user_id: string;
    [key: string]: unknown;
  };
};
