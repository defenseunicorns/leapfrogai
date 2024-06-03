import type {
  Message as OpenAIMessage,
  MessageContent
} from 'openai/resources/beta/threads/messages';
import type { Roles } from '$lib/types/threads';

export type NewMessageInput = {
  thread_id: string;
  content: string;
  role: 'user' | 'assistant';
  assistantId?: string;
};

export type LFMessage = omit<OpenAIMessage | 'content' | 'role' | 'metadata'> & {
  content: string | MessageContent[];
  role: Roles;
  metadata: {
    user_id: string;
    [key: string]: unknown;
  };
  createdAt?: Date | string | number;
};
