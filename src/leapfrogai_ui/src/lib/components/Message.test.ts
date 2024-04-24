import { render, screen } from '@testing-library/svelte';
import { vi } from 'vitest';
import { Message } from '$components/index';
import userEvent from '@testing-library/user-event';
import { getFakeMessage } from '../../testUtils/fakeData';

describe('Message component', () => {
	it('displays edit text area when edit btn is clicked', async () => {
		render(Message, { message: getFakeMessage(), handleMessageEdit: vi.fn() });
		const editPromptBtn = screen.getByRole('img', { name: /edit prompt/i });
		expect(screen.queryByText('edit message input')).not.toBeInTheDocument();
		await userEvent.click(editPromptBtn);
		await screen.findByLabelText('edit message input');
	});
	it('removes the edit textarea and restores original text on close', async () => {
		const fakeMessage = getFakeMessage();
		render(Message, { message: fakeMessage, handleMessageEdit: vi.fn() });
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
	it('submits when submit is clicked', async () => {
		const fakeSubmit = vi.fn();
		const fakeMessage = getFakeMessage();
		render(Message, { message: fakeMessage, handleMessageEdit: fakeSubmit });
		const editPromptBtn = screen.getByRole('img', { name: /edit prompt/i });
		expect(screen.queryByText('edit message input')).not.toBeInTheDocument();
		expect(screen.getByText(fakeMessage.content)).toBeInTheDocument();
		await userEvent.click(editPromptBtn);

		await userEvent.click(screen.getByRole('button', { name: /submit/i }));
		expect(fakeSubmit).toHaveBeenCalledTimes(1);
	});
	it('does not allow editing non user messages', () => {
		const fakeMessage = getFakeMessage({ role: 'assistant' });
		render(Message, { message: fakeMessage, handleMessageEdit: vi.fn() });
		expect(screen.queryByRole('img', { name: /edit prompt/i })).not.toBeInTheDocument();
	});
});
