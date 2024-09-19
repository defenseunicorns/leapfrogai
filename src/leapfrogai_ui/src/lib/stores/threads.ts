import { writable } from 'svelte/store';
import { MAX_LABEL_SIZE, NO_SELECTED_ASSISTANT_ID } from '$lib/constants';
import { goto, invalidate } from '$app/navigation';
import { error } from '@sveltejs/kit';
import { type Message as VercelAIMessage } from '@ai-sdk/svelte';
import { toastStore } from '$stores';
import type { LFThread, NewThreadInput } from '$lib/types/threads';
import type { LFMessage } from '$lib/types/messages';
import { getMessageText } from '$helpers/threads';
import { saveMessage } from '$helpers/chatHelpers';
import type { Message } from 'ai';

type ThreadsStore = {
  threads: LFThread[];
  selectedAssistantId: string;
  sendingBlocked: boolean;
  lastVisitedThreadId: string;
  streamingMessage: VercelAIMessage | null;
};

const defaultValues: ThreadsStore = {
  threads: [],
  selectedAssistantId: NO_SELECTED_ASSISTANT_ID,
  sendingBlocked: false,
  lastVisitedThreadId: '',
  streamingMessage: null
};

const createThread = async (input: NewThreadInput) => {
  const res = await fetch('/api/threads/new', {
    method: 'POST',
    body: JSON.stringify({ label: input.label.substring(0, MAX_LABEL_SIZE) }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  if (res.ok) return res.json();

  return error(500, 'Error creating thread');
};

const deleteThread = async (id: string) => {
  // A constraint on messages table will cascade delete all messages when the thread is deleted
  const res = await fetch('/api/threads/delete', {
    method: 'DELETE',
    body: JSON.stringify({ id: id }),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (res.ok) return;

  return error(500, 'Error deleting thread');
};

const deleteMessage = async (thread_id: string, message_id: string) => {
  const res = await fetch('/api/messages/delete', {
    method: 'DELETE',
    body: JSON.stringify({ thread_id, message_id }),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (res.ok) return;

  return error(500, 'Error deleting message');
};

const updateThreadLabel = async (editThreadId: string, editLabelText: string) => {
  const res = await fetch('/api/threads/update/label', {
    method: 'PUT',
    body: JSON.stringify({ id: editThreadId, label: editLabelText }),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (res.ok) return;

  return error(500, 'Error updating thread label');
};

const createThreadsStore = () => {
  const { subscribe, set, update } = writable<ThreadsStore>({ ...defaultValues });
  return {
    subscribe,
    set,
    update,
    setStreamingMessage: (message: VercelAIMessage | null) => {
      update((old) => ({ ...old, streamingMessage: message }));
    },
    setThreads: (threads: LFThread[]) => {
      update((old) => ({ ...old, threads }));
    },
    setLastVisitedThreadId: (id: string) => {
      update((old) => ({ ...old, lastVisitedThreadId: id }));
    },
    setSelectedAssistantId: (selectedAssistantId: string) => {
      update((old) => {
        return { ...old, selectedAssistantId };
      });
    },
    // Important - this method has a built in delay to ensure next user message has a different timestamp when setting to false (unblocking)
    setSendingBlocked: async (status: boolean) => {
      if (!status && process.env.NODE_ENV !== 'test') {
        new Promise((resolve) => setTimeout(resolve, 1000)).then(() => {
          update((old) => ({ ...old, sendingBlocked: status }));
        });
      } else {
        update((old) => ({ ...old, sendingBlocked: status }));
      }
    },
    changeThread: async (newId: string | null) => {
      await goto(`/chat/${newId}`);
    },
    updateThread: (newThread: LFThread) => {
      update((old) => {
        const threadIndex = old.threads.findIndex((thread) => thread.id === newThread.id);
        const threadsCopy = [...old.threads];
        threadsCopy[threadIndex] = newThread;
        return {
          ...old,
          threads: threadsCopy
        };
      });
    },
    newThread: async (label: string) => {
      try {
        const newThread = await createThread({
          label: label.substring(0, MAX_LABEL_SIZE)
        });
        if (newThread) {
          newThread.messages = [];
          update((old) => {
            return {
              ...old,
              threads: [...old.threads, newThread]
            };
          });
          await goto(`/chat/${newThread.id}`);
        }
      } catch {
        toastStore.addToast({
          kind: 'error',
          title: 'Error',
          subtitle: `Error saving thread.`
        });
      }
    },
    updateMessages: (thread_id: string, messages: LFMessage[]) => {
      update((old) => {
        const updatedThreads = [...old.threads];
        const threadIndex = old.threads.findIndex((c) => c.id === thread_id);
        const oldThread = old.threads[threadIndex];
        updatedThreads[threadIndex] = {
          ...oldThread,
          messages
        };
        return {
          ...old,
          threads: updatedThreads
        };
      });
    },
    updateMessage: (threadId: string, messageId: string, newMessage: LFMessage) => {
      update((old) => {
        const threadIndex = old.threads.findIndex((thread) => thread.id === threadId);
        if (threadIndex === -1) return old;

        const updatedThreads = [...old.threads];
        const messages = updatedThreads[threadIndex].messages;

        if (messages) {
          const messageIndex = messages.findIndex((message) => message.id === messageId);
          if (messageIndex !== -1) {
            // if message found, update it
            messages[messageIndex] = newMessage;
          }
        }

        return {
          ...old,
          threads: updatedThreads
        };
      });
    },
    addMessageToStore: async (newMessage: LFMessage) => {
      try {
        update((old) => {
          const updatedThreads = [...old.threads];
          const threadIndex = old.threads.findIndex((c) => c.id === newMessage.thread_id);
          const oldThread = old.threads[threadIndex];
          updatedThreads[threadIndex] = {
            ...oldThread,
            messages: [...(oldThread.messages || []), newMessage]
          };
          return {
            ...old,
            threads: updatedThreads
          };
        });
      } catch {
        toastStore.addToast({
          kind: 'error',
          title: 'Error',
          subtitle: `Error creating message.`
        });
      }
    },
    // The following temp empty message methods are for showing a message skeleton in the messages window
    // while waiting for a full response (e.g. waiting for translation response)
    addTempEmptyMessage: (threadId: string, tempId: string) => {
      update((old) => {
        const updatedThreads = [...old.threads];
        const threadIndex = old.threads.findIndex((c) => c.id === threadId);
        const oldThread = old.threads[threadIndex];
        updatedThreads[threadIndex] = {
          ...oldThread,
          messages: [
            ...(oldThread.messages || []),
            { id: tempId, role: 'assistant', content: '', createdAt: new Date() }
          ]
        };
        return {
          ...old,
          threads: updatedThreads
        };
      });
    },
    replaceTempMessageWithActual: (threadId: string, tempId: string, newMessage: LFMessage) => {
      update((old) => {
        const updatedThreads = [...old.threads];
        const threadIndex = old.threads.findIndex((c) => c.id === threadId);
        const tempMessageIndex = old.threads[threadIndex].messages?.findIndex(
          (m) => m.id === tempId
        );
        if (!tempMessageIndex || tempMessageIndex === -1) return old;
        const oldThread = old.threads[threadIndex];
        const messagesCopy = [...(oldThread.messages || [])];
        messagesCopy[tempMessageIndex] = newMessage;
        updatedThreads[threadIndex] = {
          ...oldThread,
          messages: messagesCopy
        };
        return {
          ...old,
          threads: updatedThreads
        };
      });
    },
    updateMessagesState: (
      originalMessages: Message[],
      setMessages: (messages: Message[]) => void,
      newMessage: LFMessage
    ) => {
      setMessages([...originalMessages, { ...newMessage, content: getMessageText(newMessage) }]);
    },
    deleteThread: async (id: string) => {
      try {
        await deleteThread(id);
        update((old) => ({
          ...old,
          threads: old.threads.filter((c) => c.id !== id)
        }));
      } catch {
        toastStore.addToast({
          kind: 'error',
          title: 'Error',
          subtitle: `Error deleting thread.`
        });
      }
    },
    deleteMessage: async (threadId: string, messageId: string) => {
      try {
        update((old) => {
          const threadIndex = old.threads.findIndex((c) => c.id === threadId);
          const thread = { ...old.threads[threadIndex] };
          thread.messages = thread.messages?.filter(
            (message: LFMessage) => message.id !== messageId
          );
          const updatedThreads = [...old.threads];
          updatedThreads[threadIndex] = thread;
          return {
            ...old,
            threads: updatedThreads
          };
        });
        await deleteMessage(threadId, messageId);
      } catch {
        toastStore.addToast({
          kind: 'error',
          title: 'Error',
          subtitle: `Error deleting message.`
        });
        await invalidate('lf:threads');
      }
    },
    updateThreadLabel: async (id: string, newLabel: string) => {
      try {
        await updateThreadLabel(id, newLabel);
        return update((old) => {
          const updatedThreadIndex = old.threads.findIndex((c) => c.id === id);
          const updatedThread = { ...old.threads[updatedThreadIndex] };
          updatedThread.metadata.label = newLabel;

          const updatedThreads = [...old.threads];
          updatedThreads[updatedThreadIndex] = updatedThread;

          return {
            ...old,
            threads: updatedThreads
          };
        });
      } catch (e) {
        toastStore.addToast({
          kind: 'error',
          title: 'Error',
          subtitle: 'Error updating label.'
        });
      }
    },
    importThreads: async (data: LFThread[]) => {
      for (const thread of data) {
        try {
          const createdThread = await createThread({
            label: thread.metadata.label
          });
          createdThread.messages = [];

          const messages = thread.messages || [];

          for (const message of messages) {
            if (message.role === 'user' || message.role === 'assistant') {
              const createdMessage = await saveMessage({
                role: message.role,
                content: getMessageText(message),
                thread_id: createdThread.id
              });
              createdThread.messages.push(createdMessage);
            }
          }

          update((old) => {
            return {
              ...old,
              threads: [...old.threads, { ...createdThread }]
            };
          });
        } catch {
          toastStore.addToast({
            kind: 'error',
            title: 'Error',
            subtitle: `Error importing thread: ${thread.metadata.label}`
          });
        }
      }
    }
  };
};

export default createThreadsStore();
