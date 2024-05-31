import { threadsStore, toastStore } from '$stores';
import { convertMessageToAiMessage, getMessageText } from '$helpers/threads';
import type { AssistantStatus, ChatRequestOptions, CreateMessage } from 'ai';
import { type Message as AIMessage } from 'ai/svelte';
import type { LFAssistant } from '$lib/types/assistants';
import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';
import { NO_SELECTED_ASSISTANT_ID } from '$constants';
import type { LFMessage, NewMessageInput } from '$lib/types/messages';
import { error } from '@sveltejs/kit';
import type { LFThread } from '$lib/types/threads';
import { tick } from 'svelte';

export const createMessage = async (input: NewMessageInput) => {
  const res = await fetch('/api/messages/new', {
    method: 'POST',
    body: JSON.stringify({
      ...input
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (res.ok) return res.json();

  return error(500, 'Error saving message');
};

export const getMessages = async (thread_id: string) => {
  const res = await fetch(`/api/messages/${thread_id}`);

  if (res.ok) return res.json();

  return error(500, 'Error saving message');
};

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
        const newMessage = await createMessage({
          thread_id: activeThreadId,
          content: getMessageText(lastMessage),
          role: lastMessage.role,
          assistantId: lastMessage.assistant_id
        });

        await threadsStore.addMessageToStore(newMessage);
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

type EditMessageArgs = {
  savedMessages: LFMessage[];
  message: Partial<OpenAIMessage>;
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
  thread_id,
  message,
  messages,
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
  const cMessage: CreateMessage = { content: getMessageText(message), role: 'user' };

  await append(cMessage, {
    data: {
      message: getMessageText(message),
      assistantId: selectedAssistantId,
      threadId: thread_id
    }
  });
};

export const handleChatMessageEdit = async ({
  savedMessages,
  message,
  messages,
  thread_id,
  setMessages,
  append
}: EditMessageArgs) => {
  if (message.id) {
    const messageIndex = messages.findIndex((m) => m.id === message.id);
    // Ensure the message after the user's message exists and is a response from the AI
    const numToSplice =
      messages[messageIndex + 1] && messages[messageIndex + 1].role !== 'user' ? 2 : 1;

    // delete old message from DB
    // savedMessages has the messages saved with the API, not the streamed messages
    // The savedMessages have actual ids (not the temp ids associated with streamed messages)
    // so we can use them to delete the messages from the db

    await threadsStore.deleteMessage(thread_id, savedMessages[messageIndex].id);
    if (numToSplice === 2) {
      // also delete that message's response
      await threadsStore.deleteMessage(thread_id, savedMessages[messageIndex + 1].id);
    }
    setMessages(messages.toSpliced(messageIndex, numToSplice)); // remove original message and response
    await tick();

    // send to /api/chat
    const cMessage: CreateMessage = {
      content: getMessageText(message),
      role: 'user',
      createdAt: new Date()
    };
    await append(cMessage);
    // Save with API
    const newMessage = await createMessage({
      thread_id,
      content: getMessageText(message),
      role: 'user'
    });

    await threadsStore.addMessageToStore(newMessage);
  }
};

export const isAssistantMessage = (message: AIMessage | OpenAIMessage) =>
  message.assistant_id && message.assistant_id !== NO_SELECTED_ASSISTANT_ID;

type HandleRegenerateArgs = {
  messages: AIMessage[];
  thread_id: string;
  setMessages: (messages: AIMessage[]) => void;
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
    body: JSON.stringify({ thread_id, message_id: response.id }),
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
    body: JSON.stringify({ thread_id, message_id: userMessage.id }),
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
  const updatedMessages = messages.filter((m) => m.id !== response.id && m.id !== userMessage.id);
  setMessages(updatedMessages);

  const createMessage: CreateMessage = {
    content: getMessageText(userMessage),
    role: 'user',
    createdAt: new Date()
  };

  await append(createMessage, {
    data: {
      message: getMessageText(userMessage),
      assistantId: response.assistant_id,
      threadId: thread_id || ''
    }
  });
};

type HandleChatRegenerateArgs = {
  savedMessages: LFMessage[];
  thread_id: string;
  message: AIMessage | OpenAIMessage;
  messages: AIMessage[] | OpenAIMessage[];
  setMessages: (messages: AIMessage[]) => void;
  reload: (
    chatRequestOptions?: ChatRequestOptions | undefined
  ) => Promise<string | null | undefined>;
};
export const handleChatRegenerate = async ({
  savedMessages,
  thread_id,
  message,
  messages,
  setMessages,
  reload
}: HandleChatRegenerateArgs) => {
  const messageIndex = messages.findIndex((m) => m.id === message.id);
  await threadsStore.deleteMessage(thread_id, savedMessages[messageIndex].id);
  setMessages(messages.toSpliced(-2, 2));
  await reload();
};

type ResetMessagesArgs = {
  activeThread?: LFThread;
  setAssistantMessages: (messages: AIMessage[]) => void;
  setChatMessages: (messages: AIMessage[]) => void;
};
// Used to reset messages when thread id changes
export const resetMessages = ({
  activeThread,
  setAssistantMessages,
  setChatMessages
}: ResetMessagesArgs) => {
  if (activeThread?.messages && activeThread.messages.length > 0) {
    const assistantMessages = activeThread.messages
      .filter((m) => m.run_id)
      .map(convertMessageToAiMessage);
    const chatMessages = activeThread.messages
      .filter((m) => !m.run_id)
      .map(convertMessageToAiMessage);

    setAssistantMessages(assistantMessages);
    setChatMessages(chatMessages);
  } else {
    setChatMessages([]);
    setAssistantMessages([]);
  }
};

// Ensure all timestamps are in unix milliseconds whether they were returned under the createdAt or created_at keys,
// and whether they are strings, numbers, or Date objects
const normalizeTimestamp = (message: AIMessage | OpenAIMessage): number => {
  const dateValue = message.createdAt || message.created_at;

  if (dateValue instanceof Date) {
    return dateValue.getTime();
  } else if (typeof dateValue === 'string') {
    return new Date(dateValue).getTime();
  } else if (typeof dateValue === 'number') {
    // Assume the timestamp is in milliseconds if it's a large number, otherwise seconds
    return dateValue > 10000000000 ? dateValue : dateValue * 1000;
  }

  return 0; // Default to 0 if no valid date is found
};

export const sortMessages = (
  messages: Array<AIMessage | OpenAIMessage>
): Array<AIMessage | OpenAIMessage> => {
  return messages.sort((a, b) => {
    const timeA = normalizeTimestamp(a);
    const timeB = normalizeTimestamp(b);
    return timeA - timeB;
  });
};

export const delay = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};
