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
import type { FileObject } from 'openai/resources/files';

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
};

export const getAssistantImage = (assistants: LFAssistant[], assistant_id: string) => {
  const myAssistant = assistants.find((assistant) => assistant.id === assistant_id);
  if (myAssistant)
    return myAssistant.metadata.avatar
      ? myAssistant.metadata.avatar
      : myAssistant.metadata.pictogram;
  return null;
};

type EditMessageArgs = {
  storeMessages: LFMessage[];
  message: Partial<OpenAIMessage | AIMessage>;
  streamedMessages: AIMessage[];
  thread_id: string;
  setStreamedMessages: (messages: AIMessage[]) => void;
  append: (
    message: AIMessage | CreateMessage,
    requestOptions?: { data?: Record<string, string> }
  ) => Promise<void>;
};

export const handleMessageEdit = async ({
  storeMessages,
  message,
  streamedMessages,
  thread_id,
  setStreamedMessages,
  append
}: EditMessageArgs) => {

  threadsStore.setSendingBlocked(true);

  if (message.id) {
    const streamedMessagesIndex = streamedMessages.findIndex((m) => m.id === message.id);
    // Ensure the message after the user's message exists and is a response from the AI
    const numToSplice =
      streamedMessages[streamedMessagesIndex + 1] && streamedMessages[streamedMessagesIndex + 1].role !== 'user'
        ? 2
        : 1;

    // delete old message from DB
    // storeMessages has the messages saved with the API, not the streamed messages
    // The storeMessages have actual ids (not the temp ids associated with streamed messages)
    // so we can use them to delete the messages from the db

    await threadsStore.deleteMessage(thread_id, storeMessages[streamedMessagesIndex].id);
    if (numToSplice === 2) {
      // also delete that message's response
      await threadsStore.deleteMessage(thread_id, storeMessages[streamedMessagesIndex + 1].id);
    }
    setStreamedMessages(streamedMessages.toSpliced(streamedMessagesIndex, numToSplice)); // remove original message and response
    await tick();

    // send to /api/chat or /api/chat/assistants
    const cMessage: CreateMessage = {
      content: getMessageText(message),
      role: 'user',
      createdAt: new Date()
    };

    if (isAssistantMessage(message)) {
      cMessage.assistant_id = message.assistant_id;
      await append(cMessage, {
        data: {
          message: getMessageText(message),
          assistantId: message.assistant_id!,
          threadId: thread_id
        }
      });
    } else {
      await append(cMessage);
      // Save with API
      const newMessage = await saveMessage({
        thread_id,
        content: getMessageText(message),
        role: 'user'
      });

      await threadsStore.addMessageToStore(newMessage);
    }
  }
};

export const isAssistantMessage = (message: Partial<AIMessage> | Partial<OpenAIMessage>) =>
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
  threadsStore.setSendingBlocked(true);
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
  storeMessages: LFMessage[];
  thread_id: string;
  message: AIMessage | OpenAIMessage;
  messages: AIMessage[] | OpenAIMessage[];
  setMessages: (messages: AIMessage[] | OpenAIMessage[]) => void;
  reload: (
    chatRequestOptions?: ChatRequestOptions | undefined
  ) => Promise<string | null | undefined>;
};
export const handleChatRegenerate = async ({
  storeMessages,
  thread_id,
  message,
  messages,
  setMessages,
  reload
}: HandleChatRegenerateArgs) => {
  threadsStore.setSendingBlocked(true);
  const messageIndex = messages.findIndex((m) => m.id === message.id);
  await threadsStore.deleteMessage(thread_id, storeMessages[messageIndex].id);
  setMessages(messages.toSpliced(-2, 2));
  await reload();
};

type ResetMessagesArgs = {
  activeThread?: LFThread;
  setAssistantMessages: (messages: AIMessage[]) => void;
  setChatMessages: (messages: AIMessage[]) => void;
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
    const assistantMessages = activeThread.messages
      .filter((m) => m.run_id)
      .map((m) => convertMessageToAiMessage(processAnnotations(m, files)));
    const chatMessages = activeThread.messages.filter((m) => !m.run_id);

    setAssistantMessages(assistantMessages);
    setChatMessages(chatMessages);
  } else {
    setChatMessages([]);
    setAssistantMessages([]);
  }
};

// Ensure all timestamps are in unix milliseconds whether they were returned under the createdAt or created_at keys,
// and whether they are strings, numbers, or Date objects
export const normalizeTimestamp = (message: AIMessage | OpenAIMessage | LFMessage): number => {
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

export const processAnnotations = (message: OpenAIMessage, files: FileObject[]) => {
  const messageCopy = { ...message };
  if (
    Array.isArray(messageCopy.content) &&
    messageCopy.content[0] !== undefined &&
    messageCopy.content[0].type === 'text'
  ) {
    let messageContent = messageCopy.content[0].text;
    const annotations = messageContent.annotations;
    const citations: string[] = [];
    // Iterate over the annotations and add footnotes
    annotations.forEach(async (annotation, index) => {
      const hasBeenProcessed = !messageContent.value.includes(annotation.text);

      if (!hasBeenProcessed) {
        // Replace the text with a footnote
        messageContent.value = messageContent.value.replace(annotation.text, ` [${index}]`);
        // Gather citations based on annotation attributes
        if (annotation.type === 'file_citation') {
          const citedFile = files.find((file) => file.id === annotation.file_citation.file_id);
          if (citedFile) {
            citations.push(`[${index}] ${citedFile.filename}`);
          }
        } else if (annotation.type === 'file_path') {
          const citedFile = files.find((file) => file.id === annotation.file_path.file_id);

          if (citedFile) {
            citations.push(`[${index}] Click <here> to download ${citedFile.filename}`);
          }
          // TODO - file download (future story)
        }
      }
    });

    // Add footnotes to the end of the message before displaying to user
    if (citations.length > 0) {
      messageContent.value += '\n\n' + citations.join('\n');
    }
  }
  return messageCopy;
};
