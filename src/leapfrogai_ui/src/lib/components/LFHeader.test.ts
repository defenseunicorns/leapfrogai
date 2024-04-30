import { render, screen } from '@testing-library/svelte';
import { LFHeader } from '$components/index';
import userEvent from '@testing-library/user-event';

describe('LFHeader', () => {
	it('closes the other header actions when one is opened', async () => {
		// We cannot test by visibility because carbon components svelte does not give us a way to grab the panel
		// in our test. The best we can do is check that the bx--header__action--active class is correctly
		// applied or not applied to the button that controls the panel
		render(LFHeader);

		const userActionBtn = screen.getByTestId('user header action button');
		await userEvent.click(userActionBtn);

		expect(userActionBtn).toHaveClass('bx--header__action--active');

		const settingsActionBtn = screen.getByTestId('settings header action button');
		await userEvent.click(settingsActionBtn);

		expect(settingsActionBtn).toHaveClass('bx--header__action--active');
		expect(userActionBtn).not.toHaveClass('bx--header__action--active');
	});
});
