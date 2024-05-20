import type { LFMessage } from '$lib/types/messages';

export const getMessageText = (message: LFMessage) => {
  if (typeof message.content === 'string') return message.content;
  if (message.content[0].type === 'text') {
    return message.content[0].text.value;
  }
  return '';
};
