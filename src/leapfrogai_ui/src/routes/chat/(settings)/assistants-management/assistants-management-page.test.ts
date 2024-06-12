import { render, screen } from '@testing-library/svelte';
import AssistantsManagementPage from './+page.svelte';
import { getFakeAssistant } from '$testUtils/fakeData';

describe('Assistants management page', () => {
  it('displays all the assistants', async () => {
    const assistant1 = getFakeAssistant();
    const assistant2 = getFakeAssistant();

    render(AssistantsManagementPage, { data: { assistants: [assistant1, assistant2] } });

    screen.getByTestId(`assistant-tile-${assistant1.name!}`);
    screen.getByTestId(`assistant-tile-${assistant2.name!}`);
  });
  // Assistant search tested with e2e
});
