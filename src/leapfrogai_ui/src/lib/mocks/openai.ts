import {
  getFakeAssistant,
  getFakeMessage,
  getFakeThread,
  getFakeVectorStore,
  getFakeVectorStoreFile
} from '$testUtils/fakeData';
import type { LFThread } from '$lib/types/threads';
import type { LFMessage } from '$lib/types/messages';
import type { LFAssistant } from '$lib/types/assistants';
import type { FileObject } from 'openai/resources/files';
import { merge } from 'lodash';
import { faker } from '@faker-js/faker';
import type { VectorStore } from 'openai/resources/beta/vector-stores/index';
import type { VectorStoreFile } from 'openai/resources/beta/vector-stores/files';

class OpenAI {
  private apiKey: string;
  private baseURL: string;
  private tempThread: LFThread;
  private threads: LFThread[];
  private tempMessage: LFMessage;
  private messages: LFMessage[];
  private assistants: LFAssistant[];
  private vectorStores: VectorStore[];
  private vectorStoreFiles: VectorStoreFile[];
  private tempAssistant: LFAssistant;
  private uploadedFiles: FileObject[];
  private errors: {
    createThread: boolean;
    updateThread: boolean;
    deleteThread: boolean;
    retrieveThread: boolean;
    retrieveMessage: boolean;
    listMessages: boolean;
    createMessage: boolean;
    deleteMessage: boolean;
    deleteAssistant: boolean;
    createAssistant: boolean;
    retrieveAssistant: boolean;
    updateAssistant: boolean;
    listAssistants: boolean;
    deleteFile: boolean;
    fileContent: boolean;
    translation: boolean;
  };

  constructor({ apiKey, baseURL }: { apiKey: string; baseURL: string }) {
    this.apiKey = apiKey;
    this.baseURL = baseURL;
    this.tempThread = getFakeThread();
    this.threads = [];
    this.tempMessage = getFakeMessage();
    this.messages = [];
    this.assistants = [];
    this.vectorStores = [];
    this.vectorStoreFiles = [];
    this.tempAssistant = getFakeAssistant();
    this.uploadedFiles = [];
    this.errors = {
      createThread: false,
      updateThread: false,
      deleteThread: false,
      retrieveThread: false,
      retrieveMessage: false,
      listMessages: false,
      createMessage: false,
      deleteMessage: false,
      createAssistant: false,
      deleteAssistant: false,
      retrieveAssistant: false,
      updateAssistant: false,
      listAssistants: false,
      deleteFile: false,
      fileContent: false,
      translation: false
    };
  }

  // Used as a test setup method to set data you want to use
  setTempThread(thread: LFThread) {
    this.tempThread = thread;
  }
  setThreads(threads: LFThread[]) {
    this.threads = threads;
  }
  setTempMessage(message: LFMessage) {
    this.tempMessage = message;
  }
  setMessages(messages: LFMessage[]) {
    this.messages = messages;
  }
  setAssistants(assistants: LFAssistant[]) {
    this.assistants = assistants;
  }
  setTempAssistant(assistant: LFAssistant) {
    this.tempAssistant = assistant;
  }
  setVectorStoreFiles(files: VectorStoreFile[]) {
    this.vectorStoreFiles = files;
  }
  setVectorStores(vectorStores: VectorStore[]) {
    this.vectorStores = vectorStores;
  }
  setFiles(files: FileObject[]) {
    this.uploadedFiles = files;
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

  audio = {
    translations: {
      create: vi.fn().mockImplementation(() => {
        if (this.errors.translation) this.throwError('translation');
        return Promise.resolve({
          text: 'Fake translation'
        });
      })
    }
  };

  files = {
    retrieve: vi.fn().mockImplementation((id) => {
      return Promise.resolve(this.uploadedFiles.find((file) => file.id === id));
    }),
    list: vi.fn().mockImplementation(() => {
      return Promise.resolve({ data: this.uploadedFiles });
    }),
    del: vi.fn().mockImplementation((id) => {
      if (this.errors.deleteFile) {
        this.resetError('deleteFile');
        return Promise.resolve({ id, object: 'file', deleted: false });
      }
      return Promise.resolve({ id, object: 'file', deleted: true });
    }),
    content: vi.fn().mockImplementation(() => {
      if (this.errors.fileContent) {
        this.resetError('fileContent');
        return Promise.reject();
      }
      return new Response(JSON.stringify({ content: 'file content' }), {
        headers: { 'Content-Type': 'application/pdf' }
      });
    })
  };

  beta = {
    threads: {
      // Create uses the "tempThread" which much be pre-set in your test
      create: vi.fn().mockImplementation(() => {
        if (this.errors.createThread) this.throwError('createThread');
        this.threads.push(this.tempThread);
        return Promise.resolve(this.tempThread);
      }),
      update: vi.fn().mockImplementation((id, body) => {
        if (this.errors.updateThread) this.throwError('updateThread');
        const threadToUpdateIndex = this.threads.findIndex((thread) => thread.id === id);
        this.threads[threadToUpdateIndex] = merge(this.threads[threadToUpdateIndex], body);

        return Promise.resolve(this.threads[threadToUpdateIndex]);
      }),
      del: vi.fn().mockImplementation((id) => {
        if (this.errors.deleteThread) {
          this.resetError('deleteThread');
          return Promise.resolve({ id, object: 'thread.deleted', deleted: false });
        }
        this.threads = this.threads.filter((thread) => thread.id !== id);
        return Promise.resolve({ id, object: 'thread.deleted', deleted: true });
      }),
      retrieve: vi.fn().mockImplementation((thread_id) => {
        if (this.errors.retrieveThread) this.throwError('retrieveThread');
        return Promise.resolve(this.threads.find((thread) => thread.id === thread_id));
      }),
      messages: {
        retrieve: vi.fn().mockImplementation((_, message_id) => {
          if (this.errors.retrieveMessage) this.throwError('retrieveMessage');
          return this.messages.find((message) => message.id === message_id);
        }),
        list: vi.fn().mockImplementation((thread_id) => {
          if (this.errors.listMessages) this.throwError('listMessages');
          return Promise.resolve({
            data: this.messages.filter((message) => message.thread_id === thread_id)
          });
        }),
        // Create uses the "tempMessage" which much be pre-set in your test
        create: vi.fn().mockImplementation(() => {
          if (this.errors.createMessage) this.throwError('createMessage');
          this.messages.push(this.tempMessage);
          return Promise.resolve(this.tempMessage);
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
          this.messages = this.messages.filter((message) => message.id !== messageId);
          return Promise.resolve({
            id: messageId,
            object: 'thread.message.deleted',
            deleted: true
          });
        })
      }
    },
    assistants: {
      // Create uses the "tempAssistant" which much be pre-set in your test
      create: vi.fn().mockImplementation(() => {
        if (this.errors.createAssistant) this.throwError('createAssistant');
        this.assistants.push(this.tempAssistant);
        return Promise.resolve(this.tempAssistant);
      }),
      list: vi.fn().mockImplementation(() => {
        if (this.errors.listAssistants) this.throwError('listAssistants');
        return Promise.resolve({ data: this.assistants });
      }),
      del: vi.fn().mockImplementation((id) => {
        if (this.errors.deleteAssistant) {
          this.resetError('deleteAssistant');
          return Promise.resolve({ id, object: 'assistant.deleted', deleted: false });
        }
        this.assistants = this.assistants.filter((assistant) => assistant.id !== id);
        return Promise.resolve({ id, object: 'assistant.deleted', deleted: true });
      }),
      retrieve: vi.fn().mockImplementation((assistant_id) => {
        if (this.errors.retrieveAssistant) this.throwError('retrieveAssistant');
        return Promise.resolve(this.assistants.find((assistant) => assistant.id === assistant_id));
      }),
      update: vi.fn().mockImplementation((id, body) => {
        if (this.errors.updateAssistant) this.throwError('updateAssistant');
        const assistantToUpdateIndex = this.assistants.findIndex(
          (assistant) => assistant.id === id
        );
        this.assistants[assistantToUpdateIndex] = merge(this.threads[assistantToUpdateIndex], body);
        return Promise.resolve(this.assistants[assistantToUpdateIndex]);
      })
    },
    vectorStores: {
      create: vi.fn().mockImplementation((body) => {
        const newVectorStore = getFakeVectorStore({ id: faker.string.uuid(), name: body.name });
        this.vectorStores.push(newVectorStore);
        return newVectorStore;
      }),
      files: {
        create: vi.fn().mockImplementation((vectorStoreId, body) => {
          const file = this.uploadedFiles.find((file) => file.id === body.file_id);
          if (file) {
            const vectorStoreFile = getFakeVectorStoreFile({
              id: body.file_id,
              vector_store_id: vectorStoreId
            });
            this.vectorStoreFiles.push(vectorStoreFile);
            return vectorStoreFile;
          }
        }),
        list: vi.fn().mockImplementation((vectorStoreId) => {
          return Promise.resolve({
            data: this.vectorStoreFiles.filter((file) => file.vector_store_id === vectorStoreId)
          });
        }),
        retrieve: vi.fn().mockImplementation((id: string) => {
          return this.vectorStoreFiles.find((file) => file.id === id);
        }),
        del: vi.fn().mockImplementation((id: string) => {
          this.vectorStoreFiles = this.vectorStoreFiles.filter((file) => file.id !== id);
          return Promise.resolve({ id, object: 'vector_store.file.deleted', deleted: true });
        })
      }
    }
  };
}

export default OpenAI;
