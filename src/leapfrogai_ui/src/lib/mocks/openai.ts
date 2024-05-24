import { getFakeAssistant, getFakeMessage, getFakeThread } from '$testUtils/fakeData';
import type { LFThread } from '$lib/types/threads';
import type { LFMessage } from '$lib/types/messages';
import type { LFAssistant } from '$lib/types/assistants';

class OpenAI {
  private apiKey: string;
  private baseURL: string;
  private thread: LFThread;
  private message: LFMessage;
  private assistant: LFAssistant;
  private errors: {
    createThread: boolean;
    updateThread: boolean;
    deleteThread: boolean;
    retrieveThread: boolean;
    createMessage: boolean;
    deleteMessage: boolean;
    deleteAssistant: boolean;
    retrieveAssistant: boolean;
    updateAssistant: boolean;
  };

  constructor({ apiKey, baseURL }: { apiKey: string; baseURL: string }) {
    this.apiKey = apiKey;
    this.baseURL = baseURL;
    this.thread = getFakeThread();
    this.message = getFakeMessage();
    this.assistant = getFakeAssistant();
    this.errors = {
      createThread: false,
      updateThread: false,
      deleteThread: false,
      retrieveThread: false,
      createMessage: false,
      deleteMessage: false,
      deleteAssistant: false,
      retrieveAssistant: false,
      updateAssistant: false
    };
  }

  // Used as a test setup method to set data you want to use
  setThread(thread: LFThread) {
    this.thread = thread;
  }
  setMessage(message: LFMessage) {
    this.message = message;
  }
  setAssistant(assistant: LFAssistant) {
    this.assistant = assistant;
  }

  setError(key: keyof typeof this.errors) {
    this.errors[key] = true;
  }

  private throwError(key: keyof typeof this.errors) {
    this.errors[key] = false; // reset
    throw new Error('Error');
  }

  private resetError(key: keyof typeof this.errors) {
    this.errors[key] = false;
  }

  beta = {
    threads: {
      create: vi.fn().mockImplementation(() => {
        if (this.errors.createThread) this.throwError('createThread');
        return Promise.resolve(this.thread);
      }),
      update: vi.fn().mockImplementation((_, body) => {
        if (this.errors.updateThread) this.throwError('updateThread');
        this.thread.metadata.label = body.metadata.label;
        return Promise.resolve(this.thread);
      }),
      del: vi.fn().mockImplementation((id) => {
        if (this.errors.deleteThread) {
          this.resetError('deleteThread');
          return Promise.resolve({ id, object: 'thread.deleted', deleted: false });
        }
        return Promise.resolve({ id, object: 'thread.deleted', deleted: true });
      }),
      retrieve: vi.fn().mockImplementation(() => {
        if (this.errors.retrieveThread) this.throwError('retrieveThread');
        return Promise.resolve(this.thread);
      }),
      messages: {
        create: vi.fn().mockImplementation(() => {
          if (this.errors.createMessage) this.throwError('createMessage');
          return Promise.resolve(this.message);
        }),
        del: vi.fn().mockImplementation((_, messageId) => {
          if (this.errors.deleteMessage) {
            this.resetError('deleteMessage');
            return Promise.resolve({
              id: messageId,
              object: 'thread.message.deleted',
              deleted: false
            });
          }
          return Promise.resolve({
            id: messageId,
            object: 'thread.message.deleted',
            deleted: true
          });
        })
      }
    },
    assistants: {
      del: vi.fn().mockImplementation((id) => {
        if (this.errors.deleteAssistant) {
          this.resetError('deleteAssistant');
          return Promise.resolve({ id, object: 'assistant.deleted', deleted: false });
        }
        return Promise.resolve({ id, object: 'assistant.deleted', deleted: true });
      }),
      retrieve: vi.fn().mockImplementation(() => {
        if (this.errors.retrieveAssistant) this.throwError('retrieveAssistant');
        return Promise.resolve(this.assistant);
      }),
      update: vi.fn().mockImplementation(() => {
        if (this.errors.updateAssistant) this.throwError('updateAssistant');
        return Promise.resolve(this.assistant);
      })
    }
  };
}

export default OpenAI;
