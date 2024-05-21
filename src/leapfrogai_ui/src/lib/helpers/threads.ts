import { type Message as AIMessage } from 'ai/svelte';
import type { Message } from 'openai/resources/beta/threads/messages';
import type { LFMessage } from '$lib/types/messages';

export const getMessageText = (message: LFMessage | Message | AIMessage) => {
  if (typeof message.content === 'string') return message.content;
  if (message.content[0].type === 'text') {
    return message.content[0].text.value;
  }
  return '';
};

export const convertMessageToAiMessage = (message: LFMessage): AIMessage => {
  return {
    ...message,
    content: getMessageText(message)
  };
};
