import { delay, http, HttpResponse } from 'msw';

import { server } from '../../../vitest-setup';
import { getFakeThread } from '$testUtils/fakeData';
import type { LFMessage } from '$lib/types/messages';

type MockChatCompletionOptions = {
  responseMsg?: string[];
  withDelay?: boolean;
  delayTime?: number;
};
export const mockChatCompletion = (
  options: MockChatCompletionOptions = {
    responseMsg: ['Fake', 'AI', 'Response'],
    withDelay: false,
    delayTime: 0
  }
) => {
  const encoder = new TextEncoder();

  server.use(
    http.post('/api/chat', async () => {
      if (options.withDelay) {
        await delay(options.delayTime);
      }
      const stream = new ReadableStream({
        start(controller) {
          options.responseMsg?.forEach((msg) => controller.enqueue(encoder.encode(msg)));
          controller.close();
        }
      });
      return new HttpResponse(stream, { headers: { 'Content-Type': 'text/plain' } });
    })
  );
};

export const mockChatCompletionError = () => {
  server.use(
    http.post('/api/chat', async () => {
      return new HttpResponse(null, { status: 500 });
    })
  );
};

export const mockNewThread = () => {
  const fakeThread = getFakeThread();
  server.use(
    http.post('/api/threads/new', () => {
      return HttpResponse.json(fakeThread);
    })
  );
};

export const mockNewMessage = (fakeMessage: LFMessage) => {
  server.use(
    http.post('/api/messages/new', () => {
      return HttpResponse.json({ message: fakeMessage });
    })
  );
};

export const mockNewThreadError = () => {
  server.use(http.post('/api/threads/new', () => new HttpResponse(null, { status: 500 })));
};
export const mockNewMessageError = () => {
  server.use(http.post('/api/messages/new', () => new HttpResponse(null, { status: 500 })));
};

export const mockDeleteThread = () => {
  server.use(http.delete('/api/threads/delete', () => new HttpResponse(null, { status: 204 })));
};

export const mockDeleteThreadError = () => {
  server.use(http.delete('/api/threads/delete', () => new HttpResponse(null, { status: 500 })));
};

export const mockEditThreadLabel = () => {
  server.use(http.put('/api/threads/update/label', () => new HttpResponse(null, { status: 204 })));
};

export const mockEditThreadLabelError = () => {
  server.use(http.put('/api/threads/update/label', () => new HttpResponse(null, { status: 500 })));
};
