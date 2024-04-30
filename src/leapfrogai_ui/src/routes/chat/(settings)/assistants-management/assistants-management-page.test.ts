import { render, screen } from '@testing-library/svelte';
import AssistantsManagementPage from './+page.svelte';
import userEvent from '@testing-library/user-event';

describe('Assistants management page', () => {
	it('displays all the assistants', async () => {
		render(AssistantsManagementPage);

		// TODO
	});
});
