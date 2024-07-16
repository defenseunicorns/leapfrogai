import { type Message as VercelAIMessage } from '@ai-sdk/svelte';
import type { Message, MessageContent } from 'openai/resources/beta/threads/messages';
import type {LFMessage, VercelOrOpenAIMessage} from '$lib/types/messages';
import { isTextContentBlock, processAnnotations } from '$helpers/chatHelpers';

export const getMessageText = (
  message: Partial<LFMessage> | Partial<VercelOrOpenAIMessage>
) => {
  if (typeof message.content === 'string') return message.content;
  if (isTextContentBlock(message.content)) {
    return processAnnotations(message.content);
  } else return '';
};

export const convertMessageToVercelAiMessage = (message: LFMessage): VercelAIMessage => {
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
