import { threadsStore, toastStore } from '$stores';
import { convertMessageToVercelAiMessage, getMessageText } from '$helpers/threads';
import type { AssistantStatus, ChatRequestOptions, CreateMessage } from 'ai';
import { type Message as VercelAIMessage } from '@ai-sdk/svelte';
import type { LFAssistant } from '$lib/types/assistants';
import type {
  Message as OpenAIMessage,
  MessageContent,
  TextContentBlock
} from 'openai/resources/beta/threads/messages';
import { NO_SELECTED_ASSISTANT_ID } from '$constants';
import type { LFMessage, NewMessageInput, VercelOrOpenAIMessage } from '$lib/types/messages';
import { error } from '@sveltejs/kit';
import type { LFThread } from '$lib/types/threads';
import { type SvelteComponent, tick } from 'svelte';
import type { FileObject } from 'openai/resources/files';
import AnnotationLink from '$components/Citation.svelte';

export const saveMessage = async (input: NewMessageInput) => {
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
  messages: VercelAIMessage[];
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
        const newMessage = await saveMessage({
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
  threadsStore.setSendingBlocked(false);
};

export const getAssistantImage = (assistants: LFAssistant[], assistant_id: string) => {
  const myAssistant = assistants.find((assistant) => assistant.id === assistant_id);
  if (myAssistant)
    return myAssistant.metadata.avatar
      ? myAssistant.metadata.avatar
      : myAssistant.metadata.pictogram;
  return null;
};

export const isRunAssistantResponse = (
  message: Partial<VercelAIMessage> | Partial<OpenAIMessage>
) =>
  'assistant_id' in message &&
  message.assistant_id &&
  message.assistant_id !== NO_SELECTED_ASSISTANT_ID;

type EditMessageArgs = {
  thread_id: string;
  messages: OpenAIMessage[];
  streamedMessages: VercelOrOpenAIMessage[];
  message: OpenAIMessage;
  setMessages: (messages: VercelAIMessage[]) => void;
  append: (
    message: VercelAIMessage | CreateMessage,
    requestOptions?: { data?: Record<string, string> }
  ) => Promise<void>;
};

export const handleMessageEdit = async ({
  thread_id,
  messages,
  streamedMessages,
  message,
  setMessages,
  append
}: EditMessageArgs) => {
  const messageIndex = messages.findIndex((m) => m.id === message.id);
  const messageResponseIndex = messageIndex + 1;
  const messageResponseId = messages[messageResponseIndex].id;
  const numToSplice =
    messages[messageResponseIndex] && messages[messageResponseIndex].role !== 'user' ? 2 : 1;

  const promises = [threadsStore.deleteMessage(thread_id, message.id)];
  if (numToSplice === 2) {
    // also delete that message's response
    promises.push(threadsStore.deleteMessage(thread_id, messageResponseId));
  }
  await Promise.all(promises).catch(() => {
    toastStore.addToast({
      kind: 'error',
      title: 'Error Editing Messages',
      subtitle: 'Message could not be edited'
    });
    return;
  });

  const indexToSplice = streamedMessages.findIndex((m) => m.id === message.id);
  setMessages(streamedMessages.toSpliced(indexToSplice, numToSplice));
  await tick();

  const cMessage: CreateMessage = {
    content: getMessageText(message),
    role: 'user',
    createdAt: new Date()
  };

  if (isRunAssistantResponse(message)) {
    cMessage.assistant_id = message.assistant_id;
    await append(cMessage, {
      data: {
        message: getMessageText(message),
        assistantId: message.assistant_id!,
        threadId: thread_id
      }
    });
  } else {
    // Save with API
    const newMessage = await saveMessage({
      thread_id,
      content: getMessageText(message),
      role: 'user'
    });
    await threadsStore.addMessageToStore(newMessage);

    await append(cMessage);
  }
};

type HandleRegenerateArgs = {
  messages: VercelAIMessage[];
  thread_id: string;
  setMessages: (messages: VercelAIMessage[]) => void;
  append: (
    message: VercelAIMessage | CreateMessage,
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
  message: VercelOrOpenAIMessage;
  messages: VercelAIMessage[];
  setMessages: (messages: VercelAIMessage[]) => void;
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
  const streamedMessageIndex = messages.findIndex((m) => m.id === message.id);
  await threadsStore.deleteMessage(thread_id, savedMessages[streamedMessageIndex].id);
  setMessages(messages.toSpliced(-2, 2));
  await reload();
};

type ResetMessagesArgs = {
  activeThread?: LFThread;
  setAssistantMessages: (messages: LFMessage[]) => void;
  setChatMessages: (messages: LFMessage[]) => void;
  files: FileObject[];
};
// Used to reset messages when thread id changes
export const resetMessages = ({
  activeThread,
  setAssistantMessages,
  setChatMessages,
  files
}: ResetMessagesArgs) => {
  if (activeThread?.messages && activeThread.messages.length > 0) {
    const parsedAssistantMessages = activeThread.messages
      .filter((m) => m.run_id)
      .map((m) => convertMessageToVercelAiMessage(m));
    const chatMessages = activeThread.messages
      .filter((m) => !m.run_id)
      .map((m) => convertMessageToVercelAiMessage(m));

    setAssistantMessages(parsedAssistantMessages);
    setChatMessages(chatMessages);
  } else {
    setChatMessages([]);
    setAssistantMessages([]);
  }
};

// Ensure all timestamps are in unix milliseconds whether they were returned under the createdAt or created_at keys,
// and whether they are strings, numbers, or Date objects
export const normalizeTimestamp = (message: VercelOrOpenAIMessage | LFMessage): number => {
  const dateValue = message.createdAt || message.created_at;

  if (dateValue instanceof Date) {
    return dateValue.getTime();
  } else if (typeof dateValue === 'string') {
    return new Date(dateValue).getTime();
  } else if (typeof dateValue === 'number') {
    // Assume the timestamp is in milliseconds if it's a large number, otherwise seconds
    return dateValue > 10000000000 ? dateValue : dateValue * 1000;
  }

  return new Date().getTime(); // Default to now
};

export const delay = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

export const isTextContentBlock = (content: MessageContent[]): content is TextContentBlock[] => {
  return Array.isArray(content) && content[0] !== undefined && content[0].type === 'text';
};

export const processAnnotations = (textContent: TextContentBlock[]) => {
  const textContentCopy = [...textContent];
  const messageContent = textContentCopy[0].text;
  const annotations = messageContent.annotations;
  annotations.forEach(async (annotation, index) => {
    const hasBeenProcessed = !messageContent.value.includes(annotation.text);
    if (!hasBeenProcessed) {
      // Replace the id with a footnote
      messageContent.value = messageContent.value.replace(annotation.text, ` [${index + 1}]`);
    }
  });
  return textContentCopy[0].text.value;
};

export const getCitations = (message: OpenAIMessage, files: FileObject[]) => {
  const messageCopy = { ...message };
  if (
    Array.isArray(messageCopy.content) &&
    messageCopy.content[0] !== undefined &&
    messageCopy.content[0].type === 'text'
  ) {
    const messageContent = messageCopy.content[0].text;
    const annotations = messageContent.annotations;
    const citations: { component: typeof SvelteComponent; props: { [key: string]: any } }[] = [];
    // Iterate over the annotations and add footnotes
    annotations.forEach(async (annotation, index) => {
      // Gather citations based on annotation attributes
      if (annotation.type === 'file_citation') {
        const citedFile = files.find((file) => file.id === annotation.file_citation.file_id);
        if (citedFile) {
          citations.push({
            component: AnnotationLink,
            props: { file: citedFile, index: index + 1 }
          });
        }
      }
    });
    return citations;
  }
  return [];
};
