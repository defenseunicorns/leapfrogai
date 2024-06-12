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

export const sortMessages = (
  messages: Array<AIMessage | OpenAIMessage>
): Array<AIMessage | OpenAIMessage> => {
  return messages.sort((a, b) => {
    const timeA = normalizeTimestamp(a);
    const timeB = normalizeTimestamp(b);
    return timeA - timeB;
  });
};

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
  allStreamedMessages: AIMessage[];
  message: Partial<OpenAIMessage>;
  messages: AIMessage[];
  thread_id: string;
  setMessages: (messages: AIMessage[]) => void;
  append: (
    message: AIMessage | CreateMessage,
    requestOptions?: { data?: Record<string, string> }
  ) => Promise<void>;
};

export const handleChatMessageEdit = async ({
  allStreamedMessages,
  message,
  messages,
  thread_id,
  setMessages,
  append
}: EditMessageArgs) => {
  if (message.id) {
    // Saved message are the completed messages returned from the API (have actual ids, not temp streamed ids)
    // Streamed chat messages will have temp ids, not actual ids. Assistant messages (even the streamed ones) have actual ids
    // When editing a streamed chat message, we have to fetch the saved messages and find the actual ids of the messages we want to delete
    // First get the index of the messages from all the streamed messages, then find the actual id using that index
    // from the saved messages
    const savedMessages = (await getMessages(thread_id)) as LFMessage[];
    sortMessages(savedMessages);

    const messagesStreamedIndex = messages.findIndex((m) => m.id === message.id);
    const allStreamedMessagesIndex = allStreamedMessages.findIndex((m) => m.id === message.id);
    const allStreamedMessagesResponseIndex = allStreamedMessagesIndex + 1;

    let savedMessageId: string | undefined = undefined;
    let savedMessageResponseId: string | undefined = undefined;

    savedMessageId = savedMessages[allStreamedMessagesIndex].id;
    savedMessageResponseId = savedMessages[allStreamedMessagesResponseIndex].id;

    // Ensure the message after the user's message exists and is a response from the AI
    const numToSplice =
      allStreamedMessages[allStreamedMessagesResponseIndex] &&
      allStreamedMessages[allStreamedMessagesResponseIndex].role !== 'user'
        ? 2
        : 1;

    // delete old message from DB
    if (savedMessageId) {
      await threadsStore.deleteMessage(thread_id, savedMessageId);
    }
    if (numToSplice === 2 && savedMessageResponseId) {
      // also delete that message's response
      await threadsStore.deleteMessage(thread_id, savedMessageResponseId);
    }
    // Update the streamed messages (subset of the streamed messages, not all the streamed messages, eg. chat or assistants)
    setMessages(messages.toSpliced(messagesStreamedIndex, numToSplice)); // remove original message and response
    await tick();

    // send to /api/chat or /api/chat/assistants
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

export const isRunAssistantResponse = (message: Partial<AIMessage> | Partial<OpenAIMessage>) =>
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
  setMessages: (messages: AIMessage[] | OpenAIMessage[]) => void;
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
      .map((m) => convertMessageToAiMessage(processAnnotations(m, files)));
    const chatMessages = activeThread.messages
      .filter((m) => !m.run_id)
      .map(convertMessageToAiMessage);

    setAssistantMessages(parsedAssistantMessages);
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
    const messageContent = messageCopy.content[0].text;
    const annotations = messageContent.annotations;
    const citations: string[] = [];
    // Iterate over the annotations and add footnotes
    annotations.forEach(async (annotation, index) => {
      const hasBeenProcessed = !messageContent.value.includes(annotation.text);

      if (!hasBeenProcessed) {
        // Replace the text with a footnote
        messageContent.value = messageContent.value.replace(annotation.text, ` [${index + 1}]`);
        // Gather citations based on annotation attributes
        if (annotation.type === 'file_citation') {
          const citedFile = files.find((file) => file.id === annotation.file_citation.file_id);
          if (citedFile) {
            citations.push(`[${index + 1}] ${citedFile.filename}`);
          }
        } else if (annotation.type === 'file_path') {
          const citedFile = files.find((file) => file.id === annotation.file_path.file_id);

          if (citedFile) {
            citations.push(`[${index + 1}] Click <here> to download ${citedFile.filename}`);
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
