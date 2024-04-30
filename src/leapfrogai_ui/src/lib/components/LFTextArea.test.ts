import { faker } from '@faker-js/faker';
import { render, screen } from '@testing-library/svelte';
import { LFTextArea } from '$components/index';
import { writable } from 'svelte/store';
import userEvent from '@testing-library/user-event';
import { afterAll, beforeAll } from 'vitest';

describe('LF Text Area', () => {
	beforeAll(() => {
		vi.mock('$env/dynamic/public', () => {
			return {
				env: {
					PUBLIC_MESSAGE_LENGTH_LIMIT: '10'
				}
			};
		});
	});

	afterAll(() => {
		vi.restoreAllMocks();
	});
	it('limits text input and displays an error message', async () => {
		const value = writable('');
		render(LFTextArea, { value, onSubmit: vi.fn(), maxRows: 2, ariaLabel: 'test input' });
		const input = screen.getByLabelText('test input');
		const limitText = faker.string.alpha({ length: 10 });
		await userEvent.type(input, limitText);
		expect(screen.queryByText('Character limit reached')).not.toBeInTheDocument();
		await userEvent.type(input, 'a');
		expect(screen.getByText('Character limit reached')).toBeInTheDocument();
		// For inputs you have to get the value by the display value, not by the screen, it won't show up on the screen
		screen.getByDisplayValue(limitText);
		expect(screen.queryByDisplayValue(`${limitText}a`)).not.toBeInTheDocument();
		await userEvent.keyboard('{backspace}');
		expect(screen.queryByText('Character limit reached')).not.toBeInTheDocument();
	});
});
