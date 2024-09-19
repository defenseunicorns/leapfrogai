import type {
  Message as OpenAIMessage,
  MessageContent
} from 'openai/resources/beta/threads/messages';
import type { Roles } from '$lib/types/threads';
import type { Message as VercelAIMessage } from '@ai-sdk/svelte';
import type { ChatRequestOptions, CreateMessage } from 'ai';

export type NewMessageInput = {
  thread_id: string;
  content?: string;
  role: 'user' | 'assistant';
  assistantId?: string;
  metadata?: unknown;
  lengthOverride?: boolean;
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

export type AppendFunction = (
  message: VercelAIMessage | CreateMessage,
  requestOptions?:
    | {
        data?: Record<string, string> | undefined;
      }
    | undefined
  // This any type matches the typing of the append function from Vercel AI
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
) => Promise<any>;

export type ReloadFunction = (
  chatRequestOptions?: ChatRequestOptions | undefined
) => Promise<string | null | undefined>;

export type VercelOrOpenAIMessage = AIMessage | OpenAIMessage;
