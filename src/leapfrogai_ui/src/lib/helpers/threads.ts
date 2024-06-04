import { type Message as AIMessage } from 'ai/svelte';
import type { Message, MessageContent } from 'openai/resources/beta/threads/messages';
import type { LFMessage } from '$lib/types/messages';

export const getMessageText = (
  message: Partial<LFMessage> | Partial<Message> | Partial<AIMessage>
) => {
  if (typeof message.content === 'string') return message.content;
  if (message.content && message.content[0] && message.content[0].type === 'text') {
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

export const convertTextToMessageContentArr = (text: string): MessageContent[] => {
  return [
    {
      text: {
        annotations: [],
        value: text
      },
      type: 'text'
    }
  ];
};
