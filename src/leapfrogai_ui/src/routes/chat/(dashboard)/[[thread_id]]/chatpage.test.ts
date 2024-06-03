import { render, screen } from '@testing-library/svelte';

import {
  fakeThreads,
  getFakeAssistant,
  getFakeOpenAIMessage,
  getFakeProfile,
  getFakeThread
} from '$testUtils/fakeData';
import ChatPage from './+page.svelte';
import ChatPageWithToast from './ChatPageWithToast.test.svelte';
import userEvent from '@testing-library/user-event';
import stores from '$app/stores';
import { afterAll, beforeAll, vi } from 'vitest';

import {
  fakeAiTextResponse,
  mockChatAssistantCompletion,
  mockChatCompletion,
  mockChatCompletionError,
  mockGetAssistants,
  mockGetMessages,
  mockNewMessage,
  mockNewMessageError
} from '$lib/mocks/chat-mocks';
import { getMessageText } from '$helpers/threads';
import { load } from './+page.server';
import {
  sessionMock,
  supabaseFromMockWrapper,
  supabaseSelectSingleByIdMock
} from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../../vitest-setup';
import type { PageData } from './$types';
import {
  ERROR_GETTING_AI_RESPONSE_TEXT,
  ERROR_GETTING_ASSISTANT_MSG_TEXT,
  ERROR_SAVING_MSG_TEXT
} from '$constants/errorMessages';
import { delay } from 'msw';
import { faker } from '@faker-js/faker';

//Calls to vi.mock are hoisted to the top of the file, so you don't have access to variables declared in the global file scope unless they are defined with vi.hoisted before the call.
const { getStores } = await vi.hoisted(() => import('$lib/mocks/svelte'));

let data: PageData;
const question = 'What is AI?';
const fakeThread = getFakeThread();

const assistant1 = getFakeAssistant();
const assistant2 = getFakeAssistant();

describe('when there is an active thread selected', () => {
  beforeAll(() => {
    vi.mock('$env/dynamic/public', () => {
      return {
        env: {
          PUBLIC_MESSAGE_LENGTH_LIMIT: '100'
        }
      };
    });

    // set active thread
    vi.mock('$app/stores', (): typeof stores => {
      const page: typeof stores.page = {
        subscribe(fn) {
          return getStores({
            url: `http://localhost/chat/${fakeThreads[0].id}`,
            params: { thread_id: fakeThreads[0].id }
          }).page.subscribe(fn);
        }
      };
      const navigating: typeof stores.navigating = {
        subscribe(fn) {
          return getStores().navigating.subscribe(fn);
        }
      };
      const updated: typeof stores.updated = {
        subscribe(fn) {
          return getStores().updated.subscribe(fn);
        },
        check: () => Promise.resolve(false)
      };

      return {
        getStores,
        navigating,
        page,
        updated
      };
    });
  });

  beforeEach(async () => {
    const allMessages = fakeThreads.flatMap((thread) => thread.messages);
    mockGetAssistants([assistant1, assistant2]);
    mockOpenAI.setThreads(fakeThreads);
    mockOpenAI.setMessages(allMessages);

    const fakeProfile = getFakeProfile({ thread_ids: fakeThreads.map((thread) => thread.id) });

    data = await load({
      fetch: global.fetch,
      locals: {
        supabase: supabaseFromMockWrapper(supabaseSelectSingleByIdMock(fakeProfile)),
        safeGetSession: sessionMock
      }
    });
  });

  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('it renders all the messages', async () => {
    render(ChatPage, { data });

    for (let i = 0; i < fakeThreads[0].messages!.length; i++) {
      await screen.findByText(getMessageText(fakeThreads[0].messages![i]));
    }
  });

  test('the send button is disabled when there is no text in the input', () => {
    render(ChatPage, { data });
    const submitBtn = screen.getByTestId('send message');
    expect(submitBtn).toHaveProperty('disabled', true);
  });

  it('submits the form then clears the input without throwing errors', async () => {
    mockChatCompletion();
    mockNewMessage();

    const { getByLabelText } = render(ChatPage, { data });

    const input = getByLabelText('message input') as HTMLInputElement;
    const submitBtn = getByLabelText('send');

    await userEvent.type(input, question);
    expect(input.value).toBe(question);

    await userEvent.click(submitBtn);

    expect(input.value).toBe('');

    expect(screen.queryByText(ERROR_GETTING_AI_RESPONSE_TEXT.subtitle!)).not.toBeInTheDocument();
  });

  it('replaces submit with a cancel button while response is being processed', async () => {
    const delayTime = 500;
    mockChatCompletion({ withDelay: true, delayTime: delayTime });
    mockNewMessage();

    const { getByLabelText } = render(ChatPage, { data });

    const input = getByLabelText('message input') as HTMLInputElement;
    const submitBtn = getByLabelText('send');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);

    expect(screen.getByTestId('cancel message')).toBeInTheDocument();

    await delay(delayTime);

    await userEvent.type(input, 'new question');
    await delay(500);
    expect(screen.queryByTestId('cancel message')).not.toBeInTheDocument();
  });

  it('disables the send button if the message length is too long', async () => {
    const { getByLabelText, getByRole } = render(ChatPage, { data });
    const input = getByLabelText('message input') as HTMLInputElement;
    const submitBtn = getByRole('button', { name: /send/i });
    const limitText = faker.string.alpha({ length: 101 });
    await userEvent.type(input, limitText);
    screen.getByDisplayValue(limitText.slice(0, -1)); // does not allow extra character
    expect(screen.getByText('Character limit reached')).toBeInTheDocument();
    expect(submitBtn).toHaveProperty('disabled', true);
  });

  it('displays a toast error notification when there is an error with the AI response', async () => {
    mockChatCompletionError();
    mockNewMessage();
    const { getByLabelText } = render(ChatPageWithToast, { data });

    const input = getByLabelText('message input') as HTMLInputElement;
    const submitBtn = getByLabelText('send');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);

    await screen.findAllByText(ERROR_GETTING_AI_RESPONSE_TEXT.subtitle!);
  });

  it('displays an error message when there is an error saving the response', async () => {
    mockChatCompletion();
    mockNewMessageError();

    const { getByLabelText } = render(ChatPageWithToast, { data });

    const input = getByLabelText('message input') as HTMLInputElement;
    const submitBtn = getByLabelText('send');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);
    await screen.findAllByText(ERROR_SAVING_MSG_TEXT.subtitle!);
  });

  it('sends a toast when a message response is cancelled', async () => {
    // Note - testing actual cancel with E2E test because the mockChatCompletion mock is no
    // setup properly yet to return the AI responses
    // Need an active thread set to ensure the call to save the message is reached

    const delayTime = 500;
    mockChatCompletion({
      withDelay: true,
      delayTime: delayTime,
      responseMsg: ['Fake', 'AI', 'Response']
    });
    mockNewMessage();

    const { getByLabelText } = render(ChatPageWithToast, { data });

    const input = getByLabelText('message input') as HTMLInputElement;
    const submitBtn = getByLabelText('send');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);
    await delay(delayTime / 2);
    const cancelBtn = screen.getByTestId('cancel message');
    await userEvent.click(cancelBtn);

    await screen.findAllByText('Response Canceled');
  });

  // Note - this doesn't test receipt of the AI response, see note at below of file
  it('can send a message with an assistant', async () => {
    mockNewMessage();
    mockChatAssistantCompletion();
    mockGetMessages([
      getFakeOpenAIMessage({ thread_id: fakeThreads[0].id, role: 'user', content: question }),
      getFakeOpenAIMessage({
        thread_id: fakeThreads[0].id,
        role: 'assistant',
        content: fakeAiTextResponse
      })
    ]);

    const { getByLabelText, getByRole, getByText } = render(ChatPage, { data });

    const assistantSelect = getByRole('button', {
      name: /select assistant open menu/i
    });
    await userEvent.click(assistantSelect);
    await userEvent.click(getByText(assistant1.name!));

    const input = getByLabelText('message input') as HTMLInputElement;
    const submitBtn = getByLabelText('send');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);

    expect(screen.queryByText(ERROR_GETTING_ASSISTANT_MSG_TEXT.subtitle!)).not.toBeInTheDocument();
  });

  // Note - Testing message editing requires an excessive amount of mocking and was deemed more practical and
  // maintainable to test with a Playwright E2E test

  // The same applies to mocking of the streamed assistant responses. A fair amount of time was spent attempting to do
  // this, but it was pretty complex and much more easily tested with an E2E
});
