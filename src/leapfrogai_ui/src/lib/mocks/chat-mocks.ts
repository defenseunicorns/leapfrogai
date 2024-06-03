import { delay, http, HttpResponse } from 'msw';

import { server } from '../../../vitest-setup';
import { fakeThreads, getFakeOpenAIMessage } from '$testUtils/fakeData';
import type { LFMessage, NewMessageInput } from '$lib/types/messages';
import type { LFAssistant } from '$lib/types/assistants';
import { AssistantResponse, createStreamDataTransformer, StreamingTextResponse } from 'ai';
import { faker } from '@faker-js/faker';

type MockChatCompletionOptions = {
  responseMsg?: string[];
  withDelay?: boolean;
  delayTime?: number;
};

export const fakeAiTextResponse = 'Fake AI Response';

const returnStreamResponse = (responseMsg: string[]) => {
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    start(controller) {
      responseMsg?.forEach((msg) => controller.enqueue(encoder.encode(`${msg} `)));
      controller.close();
    }
  });
  const streamingTextResponse = new StreamingTextResponse(
    stream.pipeThrough(createStreamDataTransformer())
  );

  return streamingTextResponse;
};
export const mockChatCompletion = (
  options: MockChatCompletionOptions = {
    responseMsg: fakeAiTextResponse.split(''),
    withDelay: false,
    delayTime: 0
  }
) => {
  server.use(
    http.post('/api/chat', async () => {
      if (options.withDelay) {
        await delay(options.delayTime);
      }
      return returnStreamResponse(options.responseMsg!);
    })
  );
};

// Note - this mock is imperfect, a fair amount of time was spent attempting to do
// mock these responses so that the useAssistant hook would work,
// but it was pretty complex and much more easily tested with an E2E
export const mockChatAssistantCompletion = (
  options: MockChatCompletionOptions = {
    responseMsg: ['Fake', 'AI', 'Response'],
    withDelay: false,
    delayTime: 0
  }
) => {
  server.use(
    http.post('/api/chat/assistants', async () => {
      if (options.withDelay) {
        await delay(options.delayTime);
      }
      return AssistantResponse(
        {
          threadId: fakeThreads[0].id,
          messageId: `msg_${faker.string.uuid()}`
        },
        vi.fn(() => Promise.resolve())
      );
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

export const mockNewMessage = () => {
  server.use(
    http.post('/api/messages/new', async ({ request }) => {
      const resJson = (await request.json()) as NewMessageInput;
      return HttpResponse.json({ message: getFakeOpenAIMessage(resJson) });
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

export const mockGetAssistants = (assistants: LFAssistant[] = []) => {
  server.use(
    http.get('/api/assistants', () => {
      return HttpResponse.json(assistants);
    })
  );
};

export const mockGetMessages = (messages: LFMessage[]) => {
  server.use(
    http.get('/api/messages', () => {
      return HttpResponse.json(messages);
    })
  );
};
