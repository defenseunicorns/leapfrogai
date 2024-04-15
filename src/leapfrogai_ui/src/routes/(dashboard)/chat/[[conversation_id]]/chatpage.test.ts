import { render, screen, within } from '@testing-library/svelte';
import { conversationsStore } from '$stores';

import {
	fakeConversations,
	getFakeConversation,
	getFakeMessage
} from '../../../../testUtils/fakeData';
import ChatPage from './+page.svelte';
import ChatPageWithToast from './ChatPageWithToast.test.svelte';
import userEvent from '@testing-library/user-event';
import stores from '$app/stores';
import { beforeAll, vi } from 'vitest';

import * as navigation from '$app/navigation';

import {
	mockChatCompletion,
	mockChatCompletionError,
	mockNewConversation,
	mockNewConversationError,
	mockNewMessage,
	mockNewMessageError
} from '$lib/mocks/chat-mocks';
import { delay } from 'msw';

//Calls to vi.mock are hoisted to the top of the file, so you don't have access to variables declared in the global file scope unless they are defined with vi.hoisted before the call.
const { getStores } = await vi.hoisted(() => import('$lib/mocks/svelte'));

describe('The Chat Page', () => {

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

		it('disables the input while a response is being processed', async () => {
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

			// submit is disabled while waiting for AI response
			expect(submitBtn).toHaveProperty('disabled', true);

			await delay(delayTime);

			await user.type(input, 'new question');
			// submit re-enabled after getting response
			expect(submitBtn).toHaveProperty('disabled', false);
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
		});
	});
});
