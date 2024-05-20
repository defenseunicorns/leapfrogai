import type { Thread } from 'openai/resources/beta/threads/threads';
import type { Message } from 'openai/resources/beta/threads/messages';

export type NewThreadInput = {
  label: string;
};

export type Roles = 'system' | 'user' | 'assistant' | 'function' | 'data' | 'tool';

export type LFThread = Thread & {
  messages?: Message[];
  metadata: {
    user_id: string;
    label: string;
    [key: string]: unknown;
  };
};
