import { render, screen } from '@testing-library/svelte';
import AssistantsManagementPage from './+page.svelte';
import { getFakeAssistant } from '$testUtils/fakeData';
import { assistantsStore } from '$stores';

describe('Assistants management page', () => {
  // Assistant search tested with e2e

  it('displays all the assistants', async () => {
    const assistant1 = getFakeAssistant();
    const assistant2 = getFakeAssistant();

    assistantsStore.setAssistants([assistant1, assistant2]);
    render(AssistantsManagementPage);

    screen.getByTestId(`assistant-card-${assistant1.name!}`);
    screen.getByTestId(`assistant-card-${assistant2.name!}`);
  });
});
