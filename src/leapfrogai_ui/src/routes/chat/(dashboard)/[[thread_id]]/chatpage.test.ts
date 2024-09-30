import { render, screen } from '@testing-library/svelte';

import { fakeThreads, getFakeAssistant, getFakeFiles } from '$testUtils/fakeData';
import ChatPage from './+page.svelte';
import ChatPageWithToast from './ChatPageWithToast.test.svelte';
import userEvent from '@testing-library/user-event';
import * as navigation from '$app/navigation';
import { afterAll, vi } from 'vitest';

import {
  fakeAiTextResponse,
  mockChatCompletion,
  mockChatCompletionError,
  mockGetAssistants,
  mockGetThread,
  mockNewMessage,
  mockNewMessageError
} from '$lib/mocks/chat-mocks';
import { getMessageText } from '$helpers/threads';
import { mockOpenAI } from '../../../../../vitest-setup';
import { ERROR_GETTING_AI_RESPONSE_TOAST, ERROR_SAVING_MSG_TOAST } from '$constants/toastMessages';

import { faker } from '@faker-js/faker';
import { delay } from '$helpers/chatHelpers';
import { mockGetFiles } from '$lib/mocks/file-mocks';
import { threadsStore } from '$stores';

const question = 'What is AI?';

const assistant1 = getFakeAssistant();
const assistant2 = getFakeAssistant();
const files = getFakeFiles();

describe('when there is an active thread selected', () => {
  beforeAll(() => {
    vi.mock('$env/dynamic/public', () => {
      return {
        env: {
          PUBLIC_MESSAGE_LENGTH_LIMIT: '100'
        }
      };
    });
  });

  beforeEach(async () => {
    const allMessages = fakeThreads.flatMap((thread) => thread.messages);
    mockGetAssistants([assistant1, assistant2]);
    mockGetFiles(files);
    mockGetThread(fakeThreads[0]);
    mockOpenAI.setThreads(fakeThreads);
    mockOpenAI.setMessages(allMessages);
    mockOpenAI.setFiles(files);

    threadsStore.set({
      threads: fakeThreads,
      lastVisitedThreadId: fakeThreads[0].id,
      sendingBlocked: false,
      streamingMessage: null
    });
  });

  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('it renders all the messages', async () => {
    render(ChatPage);

    for (let i = 0; i < fakeThreads[0].messages!.length; i++) {
      await screen.findByText(getMessageText(fakeThreads[0].messages![i]));
    }
  });

  test('the send button is disabled when there is no text in the input', () => {
    render(ChatPage);
    const submitBtn = screen.getByTestId('send message');
    expect(submitBtn).toHaveProperty('disabled', true);
  });

  it('submits the form then clears the input and gets a response without throwing errors', async () => {
    mockChatCompletion();
    mockNewMessage();

    const { getByTestId } = render(ChatPage);

    const input = getByTestId('chat-input') as HTMLInputElement;
    const submitBtn = getByTestId('send message');

    await userEvent.type(input, question);
    expect(input.value).toBe(question);

    await userEvent.click(submitBtn);

    expect(input.value).toBe('');

    expect(screen.queryByText(ERROR_GETTING_AI_RESPONSE_TOAST().subtitle!)).not.toBeInTheDocument();
    await screen.findByText(fakeAiTextResponse);
  });

  it('replaces submit with a cancel button while response is being processed', async () => {
    const delayTime = 500;
    mockNewMessage();
    mockChatCompletion({ delayTime });

    const { getByTestId } = render(ChatPage);

    const input = getByTestId('chat-input') as HTMLInputElement;
    const submitBtn = getByTestId('send message');
    await userEvent.type(input, question);
    await userEvent.click(submitBtn);

    await screen.findByTestId('cancel message');

    await screen.findByText(fakeAiTextResponse);
    await delay(delayTime);

    expect(screen.queryByTestId('cancel message')).not.toBeInTheDocument();
  });

  it('disables the send button if the message length is too long', async () => {
    const { getByTestId } = render(ChatPage);
    const input = getByTestId('chat-input') as HTMLInputElement;
    const submitBtn = getByTestId('send message');
    const limitText = faker.string.alpha({ length: 101 });
    await userEvent.type(input, limitText);
    screen.getByDisplayValue(limitText.slice(0, -1)); // does not allow extra character
    expect(screen.getByText('Character limit reached')).toBeInTheDocument();
    expect(submitBtn).toHaveProperty('disabled', true);
  });

  // TODO - this test causes the next 2 tests to fail
  it.skip('displays a toast error notification when there is an error with the AI response', async () => {
    mockChatCompletionError();
    mockNewMessage();
    const { getByTestId } = render(ChatPageWithToast);

    const input = getByTestId('chat-input') as HTMLInputElement;
    const submitBtn = getByTestId('send message');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);

    await screen.findByText(ERROR_GETTING_AI_RESPONSE_TOAST().subtitle!);
  });

  it('displays an error message when there is an error saving the response', async () => {
    mockNewMessageError();
    const { getByTestId } = render(ChatPageWithToast);

    const input = getByTestId('chat-input') as HTMLInputElement;
    const submitBtn = getByTestId('send message');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);
    await screen.findByText(ERROR_SAVING_MSG_TOAST().subtitle!);
  });

  it('sends a toast when a message response is cancelled', async () => {
    // Note - testing actual cancel with E2E test because the mockChatCompletion mock is no
    // setup properly yet to return the AI responses
    // Need an active thread set to ensure the call to save the message is reached

    const delayTime = 500;
    mockChatCompletion({
      delayTime: delayTime
    });
    mockNewMessage();

    const { getByTestId } = render(ChatPageWithToast);

    const input = getByTestId('chat-input') as HTMLInputElement;
    const submitBtn = getByTestId('send message');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);
    await delay(delayTime / 2);
    const cancelBtn = screen.getByTestId('cancel message');
    await userEvent.click(cancelBtn);

    await screen.findAllByText('Response Canceled');
  });

  it('has a button to go to the assistants management page in the assistant dropdown', async () => {
    const goToSpy = vi.spyOn(navigation, 'goto');

    const { getByRole, getByTestId } = render(ChatPage);

    const assistantSelect = getByTestId('assistants-select-btn');
    await userEvent.click(assistantSelect);
    await userEvent.click(
      getByRole('button', {
        name: /manage assistants/i
      })
    );

    expect(goToSpy).toHaveBeenCalledTimes(1);
    expect(goToSpy).toHaveBeenCalledWith(`/chat/assistants-management`);
  });

  // Note - Testing message editing requires an excessive amount of mocking and was deemed more practical and
  // maintainable to test with a Playwright E2E test

  // The same applies to mocking of the streamed assistant responses. A fair amount of time was spent attempting to do
  // this, but it was pretty complex and much more easily tested with an E2E
});
