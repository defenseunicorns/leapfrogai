import { render, screen } from '@testing-library/svelte';
import { afterAll, afterEach, type MockInstance, vi } from 'vitest';
import { Message } from '$components/index';
import userEvent from '@testing-library/user-event';
import { getFakeMessage } from '../../testUtils/fakeData';
import MessageWithToast from '$components/MessageWithToast.test.svelte';

const fakeHandleMessageEdit = vi.fn();
const fakeHandleRegenerate = vi.fn();

const defaultMessageProps = {
	message: getFakeMessage(),
	handleMessageEdit: fakeHandleMessageEdit,
	handleRegenerate: fakeHandleRegenerate,
	isLastMessage: false,
	isLoading: false
};

describe('Message component', () => {
	afterEach(() => {
		fakeHandleMessageEdit.mockReset();
		fakeHandleRegenerate.mockReset();
	});

	afterAll(() => {
		fakeHandleMessageEdit.mockRestore();
		fakeHandleRegenerate.mockRestore();
	});
	it('displays edit text area when edit btn is clicked', async () => {
		render(Message, { ...defaultMessageProps });
		expect(screen.queryByText('edit message input')).not.toBeInTheDocument();
		const editPromptBtn = screen.getByRole('img', { name: /edit prompt/i });
		await userEvent.click(editPromptBtn);
		await screen.findByLabelText('edit message input');
	});
	it('removes the edit textarea and restores original text on close', async () => {
		const fakeMessage = getFakeMessage();
		render(Message, { ...defaultMessageProps, message: fakeMessage });
		const editPromptBtn = screen.getByRole('img', { name: /edit prompt/i });
		expect(screen.queryByText('edit message input')).not.toBeInTheDocument();
		expect(screen.getByText(fakeMessage.content)).toBeInTheDocument();
		await userEvent.click(editPromptBtn);

		const input = screen.getByRole('textbox', { name: /edit message input/i });
		await userEvent.clear(input);
		expect(screen.queryByText(fakeMessage.content)).not.toBeInTheDocument();

		await userEvent.click(screen.getByRole('button', { name: /cancel/i }));
		expect(screen.getByText(fakeMessage.content)).toBeInTheDocument();
	});
	it('submits message edit when submit is clicked', async () => {
		const fakeMessage = getFakeMessage();
		render(Message, { ...defaultMessageProps, message: fakeMessage });
		const editPromptBtn = screen.getByRole('img', { name: /edit prompt/i });
		expect(screen.queryByText('edit message input')).not.toBeInTheDocument();
		expect(screen.getByText(fakeMessage.content)).toBeInTheDocument();
		await userEvent.click(editPromptBtn);

		await userEvent.click(screen.getByRole('button', { name: /submit/i }));
		expect(fakeHandleMessageEdit).toHaveBeenCalledTimes(1);
	});
	it('does not allow editing non user messages', () => {
		const fakeAssistantMessage = getFakeMessage({ role: 'assistant' });
		render(Message, { ...defaultMessageProps, message: fakeAssistantMessage });
		expect(screen.queryByRole('img', { name: /edit prompt/i })).not.toBeInTheDocument();
	});

	describe('util functions', () => {
		let clipboardSpy: MockInstance;

		afterAll(() => {
			clipboardSpy.mockRestore();
		});

		it('copies text of AI response to clipboard and sends a toast notification', async () => {
			Object.assign(navigator, {
				clipboard: { writeText: vi.fn().mockImplementation(() => Promise.resolve()) }
			});

			clipboardSpy = vi.spyOn(navigator.clipboard, 'writeText');
			const fakeAssistantMessage = getFakeMessage({ role: 'assistant' });
			render(MessageWithToast, {
				...defaultMessageProps,
				message: fakeAssistantMessage
			});

			await userEvent.click(screen.getByLabelText('copy message'));

			expect(clipboardSpy).toHaveBeenCalledTimes(1);
			expect(clipboardSpy).toHaveBeenCalledWith(fakeAssistantMessage.content);
			await screen.findByText('Response message copied.');
		});
		it('sends an error toast notification if there is an error copying text', async () => {
			Object.assign(navigator, {
				clipboard: { writeText: vi.fn().mockImplementation(() => Promise.reject()) }
			});

			clipboardSpy = vi.spyOn(navigator.clipboard, 'writeText');
			const fakeAssistantMessage = getFakeMessage({ role: 'assistant' });
			render(MessageWithToast, {
				...defaultMessageProps,
				message: fakeAssistantMessage
			});

			await userEvent.click(screen.getByLabelText('copy message'));

			await screen.findByText('Error copying text.');
		});

		it('disables edit submit button when message is loading', async () => {
			render(MessageWithToast, {
				...defaultMessageProps,
				isLoading: true
			});

			const editPromptBtn = screen.getByRole('img', { name: /edit prompt/i });
			await userEvent.click(editPromptBtn);

			const submitBtn = screen.getByRole('button', { name: /submit/i });
			expect(submitBtn).toHaveProperty('disabled', true);
		});
		it('has copy and regenerate buttons for the last AI response', () => {
			render(MessageWithToast, {
				...defaultMessageProps,
				message: getFakeMessage({ role: 'assistant' }),
				isLastMessage: true
			});

			expect(screen.getByLabelText('copy message'));
			expect(screen.getByLabelText('regenerate message'));
		});
		it('does not have regenerate buttons for user messages', () => {
			render(MessageWithToast, {
				...defaultMessageProps,
				message: getFakeMessage({ role: 'user' }),
				isLastMessage: true
			});

			expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
		});
		it('does not have regenerate buttons for AI responses that are not the last response', () => {
			render(MessageWithToast, {
				...defaultMessageProps,
				message: getFakeMessage({ role: 'assistant' }),
				isLastMessage: false
			});

			expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
		});
		it('does not have a copy button for user messages', () => {
			render(MessageWithToast, {
				...defaultMessageProps,
				message: getFakeMessage({ role: 'user' })
			});

			expect(screen.queryByLabelText('copy message')).not.toBeInTheDocument();
		});
		it('removes the copy and regenerate buttons when a response is loading', () => {
			render(MessageWithToast, {
				...defaultMessageProps,
				message: getFakeMessage({ role: 'assistant' }),
				isLastMessage: true,
				isLoading: true
			});
			expect(screen.queryByLabelText('copy message')).not.toBeInTheDocument();
			expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
		});
	});
});
