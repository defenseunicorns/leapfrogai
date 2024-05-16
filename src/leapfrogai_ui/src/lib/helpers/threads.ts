import type {LFMessage} from "$lib/types/messages";

export const getMessageText = (message: LFMessage) => {
    if (typeof message.content === 'string') return message.content;
    if (typeof message.content[0] === 'object') {
        return message.content[0].text.value;
    }
    return '';
};