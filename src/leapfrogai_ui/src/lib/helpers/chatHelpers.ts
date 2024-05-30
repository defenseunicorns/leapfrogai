import { threadsStore, toastStore } from '$stores';
import { getMessageText } from '$helpers/threads';
import type { AssistantStatus, ChatRequestOptions, CreateMessage } from 'ai';
import { type Message as AIMessage } from 'ai/svelte';
import type { LFAssistant } from '$lib/types/assistants';
import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';
import { NO_SELECTED_ASSISTANT_ID } from '$constants';

type StopThenSaveArgs = {
  activeThreadId: string;
  messages: AIMessage[];
  status: AssistantStatus;
  isLoading: boolean;
  assistantStop: () => void;
  chatStop: () => void;
};
export const stopThenSave = async ({
  activeThreadId,
  messages,
  status,
  isLoading,
  assistantStop,
  chatStop
}: StopThenSaveArgs) => {
  // Note - assistantStop does not cancel the actual run, it only stops the stream
  // If you try to send another message while the run is still running on the server,
  // you will get an error.
  // issue opened for this here: https://github.com/vercel/ai/issues/1743
  if (status === 'in_progress') assistantStop();
  else {
    if (isLoading) {
      chatStop();
      const lastMessage = messages[messages.length - 1];

      if (activeThreadId && lastMessage.role !== 'user') {
        await threadsStore.newMessage({
          thread_id: activeThreadId,
          content: getMessageText(lastMessage), // save last message
          role: lastMessage.role
        });
      }
    }
  }

  toastStore.addToast({
    kind: 'info',
    title: 'Response Canceled',
    subtitle: 'Response generation canceled.'
  });
};

export const getAssistantImage = (assistants: LFAssistant[], assistant_id: string) => {
  const myAssistant = assistants.find((assistant) => assistant.id === assistant_id);
  if (myAssistant) return myAssistant.metadata.avatar ?? myAssistant.metadata.pictogram;
  return null;
};

// TODO - create reg message, create assistant message, create regular message, order gets messed up
// TODO - there's a sequence of events that that removes the assistant from an edited message

type EditMessageArgs = {
  message: AIMessage | OpenAIMessage;
  messages: AIMessage[];
  thread_id: string;
  setMessages: (messages: AIMessage[]) => void;
  append: (
    message: AIMessage | CreateMessage,
    requestOptions?: { data?: Record<string, string> }
  ) => Promise<void>;
};
type EditAssistantMessageArgs = EditMessageArgs & { selectedAssistantId: string };

export const handleAssistantMessageEdit = async ({
  selectedAssistantId,
  message,
  messages,
  thread_id,
  setMessages,
  append
}: EditAssistantMessageArgs) => {
  const messageIndex = messages.findIndex((m) => m.id === message.id);
  // Ensure the message after the user's message exists and is a response from the AI
  const numToSplice =
    messages[messageIndex + 1] && messages[messageIndex + 1].role !== 'user' ? 2 : 1;

  const deleteRes1 = await fetch('/api/messages/delete', {
    method: 'DELETE',
    body: JSON.stringify({ thread_id, message_id: message.id }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  if (!deleteRes1.ok) {
    toastStore.addToast({
      kind: 'error',
      title: 'Error Editing Message',
      subtitle: 'Editing cancelled'
    });
    return;
  }

  if (numToSplice === 2) {
    const deleteRes2 = await fetch('/api/messages/delete', {
      method: 'DELETE',
      body: JSON.stringify({
        thread_id,
        message_id: messages[messageIndex + 1].id
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    });
    if (!deleteRes2.ok) {
      toastStore.addToast({
        kind: 'error',
        title: 'Error Editing Message',
        subtitle: 'Editing Cancelled'
      });
      return;
    }
  }
  setMessages(messages.toSpliced(messageIndex, numToSplice));
  // send to /api/chat/assistants
  const createMessage: CreateMessage = { content: getMessageText(message), role: 'user' };
  await append(createMessage, {
    data: {
      message: getMessageText(message),
      assistantId: selectedAssistantId,
      threadId: thread_id
    }
  });
};

export const handleChatMessageEdit = async ({
  message,
  messages,
  thread_id,
  setMessages,
  append
}: EditMessageArgs) => {
  const messageIndex = messages.findIndex((m) => m.id === message.id);
  // Ensure the message after the user's message exists and is a response from the AI
  const numToSplice =
    messages[messageIndex + 1] && messages[messageIndex + 1].role !== 'user' ? 2 : 1;

  if (thread_id) {
    // delete old message from DB
    await threadsStore.deleteMessage(thread_id, message.id);
    if (numToSplice === 2) {
      // also delete that message's response
      await threadsStore.deleteMessage(thread_id, messages[messageIndex + 1].id);
    }

    // save new message
    await threadsStore.newMessage({
      thread_id,
      content: getMessageText(message),
      role: 'user'
    });
  }
  setMessages(messages.toSpliced(messageIndex, numToSplice)); // remove original message and response

  // send to /api/chat
  const createMessage: CreateMessage = { content: getMessageText(message), role: 'user' };
  await append(createMessage);
};

export const isAssistantMessage = (message: AIMessage | OpenAIMessage) =>
  message.assistant_id && message.assistant_id !== NO_SELECTED_ASSISTANT_ID;

type HandleRegenerateArgs = {
  messages: AIMessage[] | OpenAIMessage[];
  thread_id: string;
  setMessages: (messages: Array<AIMessage | OpenAIMessage>) => void;
  append: (
    message: AIMessage | CreateMessage,
    requestOptions?: { data?: Record<string, string> }
  ) => Promise<void>;
};
export const handleAssistantRegenerate = async ({
  messages,
  setMessages,
  thread_id,
  append
}: HandleRegenerateArgs) => {
  const lastMessageIndex = messages.length - 1;
  const userMessage = messages[lastMessageIndex - 1];
  const response = messages[lastMessageIndex];

  // useAssistant doesn't have a reload function, so we delete both the user message and the assistant response,
  // then manually append
  const deleteRes1 = await fetch('/api/messages/delete', {
    method: 'DELETE',
    body: JSON.stringify({ thread_id: thread_id, message_id: response.id }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  if (!deleteRes1.ok) {
    toastStore.addToast({
      kind: 'error',
      title: 'Error Regenerating Message',
      subtitle: 'Regeneration cancelled'
    });
    return;
  }
  const deleteRes2 = await fetch('/api/messages/delete', {
    method: 'DELETE',
    body: JSON.stringify({ thread_id: thread_id, message_id: userMessage.id }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  if (!deleteRes2.ok) {
    toastStore.addToast({
      kind: 'error',
      title: 'Error Regenerating Message',
      subtitle: 'Regeneration cancelled'
    });
    return;
  }
  setMessages(messages.toSpliced(-2, 2));

  await append(
    { ...userMessage, createdAt: undefined },
    {
      data: {
        message: userMessage.content,
        assistantId: response.assistant_id,
        threadId: thread_id || ''
      }
    }
  );
};

type HandleChatRegenerateArgs = {
  thread_id: string;
  message: AIMessage | OpenAIMessage;
  messages: AIMessage[] | OpenAIMessage[];
  setMessages: (messages: Array<AIMessage | OpenAIMessage>) => void;
  reload: (
    chatRequestOptions?: ChatRequestOptions | undefined
  ) => Promise<string | null | undefined>;
};
export const handleChatRegenerate = async ({
  thread_id,
  message,
  messages,
  setMessages,
  reload
}: HandleChatRegenerateArgs) => {
  await threadsStore.deleteMessage(thread_id, message.id);
  setMessages(messages.toSpliced(-2, 2));
  await reload();
};
