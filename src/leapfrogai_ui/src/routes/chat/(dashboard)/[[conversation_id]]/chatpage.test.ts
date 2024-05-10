import { render, screen } from '@testing-library/svelte';
import { conversationsStore } from '$stores';

import {
  fakeConversations,
  getFakeConversation,
  getFakeMessage
} from '../../../../../testUtils/fakeData';
import ChatPage from './+page.svelte';
import ChatPageWithToast from './ChatPageWithToast.test.svelte';
import userEvent from '@testing-library/user-event';
import stores from '$app/stores';
import { afterAll, beforeAll, vi } from 'vitest';

import {
  mockChatCompletion,
  mockChatCompletionError,
  mockNewConversation,
  mockNewConversationError,
  mockNewMessage,
  mockNewMessageError
} from '$lib/mocks/chat-mocks';
import { delay } from 'msw';
import { faker } from '@faker-js/faker';

//Calls to vi.mock are hoisted to the top of the file, so you don't have access to variables declared in the global file scope unless they are defined with vi.hoisted before the call.
const { getStores } = await vi.hoisted(() => import('$lib/mocks/svelte'));

describe('The Chat Page', () => {
  beforeAll(() => {
    vi.mock('$env/dynamic/public', () => {
      return {
        env: {
          PUBLIC_MESSAGE_LENGTH_LIMIT: '100'
        }
      };
    });
  });

  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('it renders all the messages', async () => {
    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatPage);

    for (let i = 0; i < fakeConversations[0].messages.length; i++) {
      await screen.findByText(fakeConversations[0].messages[0].content);
    }
  });

  describe('chat form', () => {
    const question = 'What is AI?';
    const fakeConversation = getFakeConversation();
    const fakeMessage = getFakeMessage({
      role: 'user',
      conversation_id: fakeConversation.id,
      user_id: fakeConversation.user_id,
      content: question
    });

    test('the send button is disabled when there is no text in the input', () => {
      render(ChatPage);
      const submitBtn = screen.getByTestId('send message');
      expect(submitBtn).toHaveProperty('disabled', true);
    });

    it('submits the form then clears the input without throwing errors', async () => {
      mockNewConversation();
      mockChatCompletion();
      mockNewMessage(fakeMessage);

      conversationsStore.set({
        conversations: []
      });

      const user = userEvent.setup();

      const { getByLabelText } = render(ChatPage);

      const input = getByLabelText('message input') as HTMLInputElement;
      const submitBtn = getByLabelText('send');

      await user.type(input, question);
      expect(input.value).toBe(question);

      await user.click(submitBtn);

      expect(input.value).toBe('');
    });

    it('replaces submit with a cancel button while response is being processed', async () => {
      const delayTime = 500;
      mockNewConversation();
      mockChatCompletion({ withDelay: true, delayTime: delayTime });
      mockNewMessage(fakeMessage);

      conversationsStore.set({
        conversations: []
      });

      const user = userEvent.setup();

      const { getByLabelText } = render(ChatPage);

      const input = getByLabelText('message input') as HTMLInputElement;
      const submitBtn = getByLabelText('send');

      await user.type(input, question);
      await user.click(submitBtn);

      expect(screen.getByTestId('cancel message')).toBeInTheDocument();

      await delay(delayTime);

      await user.type(input, 'new question');
      expect(screen.queryByTestId('cancel message')).not.toBeInTheDocument();
    });

    it('disables the send button if the message length is too long', async () => {
      const { getByLabelText, getByRole } = render(ChatPage);
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
      mockNewConversation();

      const user = userEvent.setup();
      const { getByLabelText } = render(ChatPageWithToast);

      const input = getByLabelText('message input') as HTMLInputElement;
      const submitBtn = getByLabelText('send');

      await user.type(input, question);
      await user.click(submitBtn);

      await screen.findAllByText('Error getting AI Response');
    });

    it('displays an error message when there is an error saving the new conversation', async () => {
      conversationsStore.set({
        conversations: []
      });

      mockChatCompletion();
      mockNewConversationError();

      const { getByLabelText } = render(ChatPageWithToast);

      const input = getByLabelText('message input') as HTMLInputElement;
      const submitBtn = getByLabelText('send');

      await userEvent.type(input, question);
      await userEvent.click(submitBtn);
      await screen.findAllByText('Error saving conversation.');
    });

    describe('when there is an active conversation selected', () => {
      beforeAll(() => {
        vi.mock('$app/stores', (): typeof stores => {
          const page: typeof stores.page = {
            subscribe(fn) {
              return getStores({
                url: `http://localhost/chat/${fakeConversations[0].id}`,
                params: { conversation_id: fakeConversations[0].id }
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

      it('displays an error message when there is an error saving the response', async () => {
        conversationsStore.set({
          conversations: fakeConversations
        });

        mockChatCompletion();
        mockNewMessageError();

        const { getByLabelText } = render(ChatPageWithToast);

        const input = getByLabelText('message input') as HTMLInputElement;
        const submitBtn = getByLabelText('send');

        await userEvent.type(input, question);
        await userEvent.click(submitBtn);
        await screen.findAllByText('Error creating message.');
      });
      it('sends a toast when a message response is cancelled', async () => {
        // Note - testing actual cancel with E2E test because the mockChatCompletion mock is no
        // setup properly yet to return the AI responses
        // Need an active conversation set to ensure the call to save the message is reached
        vi.mock('$app/stores', (): typeof stores => {
          const page: typeof stores.page = {
            subscribe(fn) {
              return getStores({
                url: `http://localhost/chat/${fakeConversations[0].id}`,
                params: { conversation_id: fakeConversations[0].id }
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

        const delayTime = 500;
        mockNewConversation();
        mockChatCompletion({
          withDelay: true,
          delayTime: delayTime,
          responseMsg: ['Fake', 'AI', 'Response']
        });
        mockNewMessage(fakeMessage);

        conversationsStore.set({
          conversations: [fakeConversations[0]]
        });
        const user = userEvent.setup();

        const { getByLabelText } = render(ChatPageWithToast);

        const input = getByLabelText('message input') as HTMLInputElement;
        const submitBtn = getByLabelText('send');

        await user.type(input, question);
        await user.click(submitBtn);
        await delay(delayTime / 2);
        const cancelBtn = screen.getByTestId('cancel message');
        await user.click(cancelBtn);

        await screen.findAllByText('Response Canceled');
      });
    });

    // Note - Testing message editing requires an excessive amount of mocking and was deemed more practical and
    // maintainable to test with a Playwright E2E test
  });
});
