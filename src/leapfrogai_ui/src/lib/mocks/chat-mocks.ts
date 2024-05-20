import { http, HttpResponse, delay } from 'msw';
import { faker } from '@faker-js/faker';
import { server } from '../../../vitest-setup';

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

export const mockNewConversation = () => {
  server.use(
    http.post('/api/conversations/new', () => {
      return HttpResponse.json({
        id: faker.string.uuid(),
        user_id: faker.string.uuid(),
        label: faker.lorem.words(5),
        created_at: new Date()
      });
    })
  );
};

export const mockNewMessage = (fakeMessage: Message) => {
  server.use(
    http.post('/api/messages/new', () => {
      return HttpResponse.json({ message: fakeMessage });
    })
  );
};

export const mockNewConversationError = () => {
  server.use(http.post('/api/conversations/new', () => new HttpResponse(null, { status: 500 })));
};
export const mockNewMessageError = () => {
  server.use(http.post('/api/messages/new', () => new HttpResponse(null, { status: 500 })));
};

export const mockDeleteConversation = () => {
  server.use(
    http.delete('/api/conversations/delete', () => new HttpResponse(null, { status: 204 }))
  );
};

export const mockDeleteConversationError = () => {
  server.use(
    http.delete('/api/conversations/delete', () => new HttpResponse(null, { status: 500 }))
  );
};

export const mockEditConversationLabel = () => {
  server.use(
    http.put('/api/conversations/update/label', () => new HttpResponse(null, { status: 204 }))
  );
};

export const mockEditConversationLabelError = () => {
  server.use(
    http.put('/api/conversations/update/label', () => new HttpResponse(null, { status: 500 }))
  );
};
