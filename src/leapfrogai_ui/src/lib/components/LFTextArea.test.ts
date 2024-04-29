import { faker } from '@faker-js/faker';
import { render, screen } from '@testing-library/svelte';
import { LFTextArea } from '$components/index';
import { writable } from 'svelte/store';
import userEvent from '@testing-library/user-event';

const lengthOverride = 10;
describe('LF Text Area', () => {

    // beforeAll(() => {
    //     process.env.PUBLIC_MESSAGE_LENGTH_LIMIT = `${lengthOverride}`;
    // });

	it('limits text input and displays an error message', async () => {
		let value = writable('');
		render(LFTextArea, { value, onSubmit: vi.fn(), maxRows: 2 });
		const input = screen.getByLabelText('message input');
		await userEvent.type(input, faker.string.alpha({length: lengthOverride}));
        expect(screen.queryByText('Character limit reached')).not.toBeInTheDocument();
        await userEvent.type(input, "a");
        expect(screen.getByText('Character limit reached')).toBeInTheDocument();

	});
});
