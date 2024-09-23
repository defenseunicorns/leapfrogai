import { delay, http, HttpResponse } from 'msw';
import { server } from '../../../vitest-setup';
import { getFakeOpenAIMessage } from '$testUtils/fakeData';
import type { LFMessage, NewMessageInput } from '$lib/types/messages';
import type { LFAssistant } from '$lib/types/assistants';
import { createStreamDataTransformer, StreamingTextResponse } from 'ai';
import type { LFThread } from '$lib/types/threads';
import { AUDIO_FILE_SIZE_ERROR_TEXT } from '$constants';

type MockChatCompletionOptions = {
  responseMsg?: string[];
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
  return new StreamingTextResponse(stream.pipeThrough(createStreamDataTransformer()));
};
export const mockChatCompletion = (options: MockChatCompletionOptions = {}) => {
  const { delayTime = 0, responseMsg = ['Fake', 'AI', 'Response'] } = options;
  server.use(
    http.post('/api/chat', async () => {
      if (delayTime) {
        await delay(delayTime);
      }
      return returnStreamResponse(responseMsg!);
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
      const reqJson = (await request.json()) as NewMessageInput;
      return HttpResponse.json(getFakeOpenAIMessage(reqJson));
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

export const mockGetMessages = (thread_id: string, messages: LFMessage[]) => {
  server.use(
    http.get(`/api/messages/${thread_id}`, () => {
      return HttpResponse.json(messages);
    })
  );
};

export const mockGetThread = (thread: LFThread) => {
  server.use(
    http.get(`/api/threads/${thread.id}`, () => {
      return HttpResponse.json(thread);
    })
  );
};

export const mockTranslation = ({ delay: delayTime = 0 } = {}) => {
  server.use(
    http.post('/api/audio/translation', async () => {
      if (delayTime) {
        await delay(delayTime);
      }
      return HttpResponse.json({ text: 'fake translation' });
    })
  );
};

export const mockTranslationError = () => {
  server.use(
    http.post('/api/audio/translation', () => {
      return new HttpResponse(null, { status: 500 });
    })
  );
};

export const mockTranslationFileSizeError = () => {
  server.use(
    http.post('/api/audio/translation', () => {
      return HttpResponse.json(
        { message: `ValidationError: ${AUDIO_FILE_SIZE_ERROR_TEXT}` },
        { status: 400 }
      );
    })
  );
};

export const mockTranscription = ({ delay: delayTime = 0 } = {}) => {
  server.use(
    http.post('/api/audio/transcription', async () => {
      if (delayTime) {
        await delay(delayTime);
      }
      return HttpResponse.json({ text: 'fake transcription' });
    })
  );
};

export const mockTranscriptionError = () => {
  server.use(
    http.post('/api/audio/transcription', () => {
      return new HttpResponse(null, { status: 500 });
    })
  );
};

export const mockTranscriptionFileSizeError = () => {
  server.use(
    http.post('/api/audio/transcription', () => {
      return HttpResponse.json(
        { message: `ValidationError: ${AUDIO_FILE_SIZE_ERROR_TEXT}` },
        { status: 400 }
      );
    })
  );
};
