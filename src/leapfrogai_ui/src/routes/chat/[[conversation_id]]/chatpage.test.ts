import { render, screen } from '@testing-library/svelte';
import { conversationsStore } from '$stores';

import {
	fakeConversations,
	getFakeConversation,
	getFakeMessage
} from '../../../testUtils/fakeData';
import ChatPage from './+page.svelte';
import ChatPageWithToast from './ChatPageWithToast.test.svelte';
import userEvent from '@testing-library/user-event';
import stores from '$app/stores';
import { afterEach, vi } from 'vitest';

import * as navigation from '$app/navigation';

import {
	mockChatCompletion,
	mockChatCompletionError,
	mockNewConversation,
	mockNewMessage
} from '$lib/mocks/chat-mocks';
import { delay } from 'msw';

const { getStores } = await vi.hoisted(() => import('../../../lib/mocks/svelte'));

describe('The Chat Page', () => {
	afterEach(() => {
		vi.resetAllMocks();
	});
	it('changes the active chat thread', async () => {
		const goToSpy = vi.spyOn(navigation, 'goto');

		const fakeConversation = getFakeConversation({ numMessages: 6 });

		conversationsStore.set({
			conversations: [fakeConversation]
		});

		render(ChatPage);

		expect(screen.queryByText(fakeConversation.messages[0].content)).not.toBeInTheDocument();

		await userEvent.click(screen.getByText(fakeConversation.label));

		expect(goToSpy).toHaveBeenCalledTimes(1);
		expect(goToSpy).toHaveBeenCalledWith(`/chat/${fakeConversation.id}`);
	});

	it('it renders all the messages', async () => {
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

		conversationsStore.set({
			conversations: fakeConversations
		});

		render(ChatPage);

		// The test does show that the conversation_id and activeConversation are being set correctly
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
			const submitBtn = screen.getByLabelText('send');
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

			expect(screen.getByLabelText('cancel')).toBeInTheDocument();

			await delay(delayTime);

			await user.type(input, 'new question');
			expect(screen.queryByLabelText('cancel')).not.toBeInTheDocument();
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
			const cancelBtn = screen.getByLabelText('cancel');
			await user.click(cancelBtn);

			await screen.findAllByText('Response Canceled');
		});
	});
});
