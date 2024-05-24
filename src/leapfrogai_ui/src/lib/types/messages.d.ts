import type { Message, MessageContent } from 'openai/resources/beta/threads/messages';
import type { Roles } from '$lib/types/threads';

export type NewMessageInput = {
  thread_id: string;
  content: string;
  role: 'user' | 'assistant';
  assistantId?: string;
};

export type LFMessage = Message & {
  content: string | MessageContent[];
  role: Roles;
  metadata: {
    user_id: string;
    [key: string]: unknown;
  };
};
