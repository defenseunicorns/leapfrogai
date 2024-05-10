import { render, screen } from '@testing-library/svelte';
import AssistantsManagementPage from './+page.svelte';
import { getFakeAssistant } from '../../../../../testUtils/fakeData';
import { assistantsStore } from '$stores';

describe('Assistants management page', () => {
  it('displays all the assistants', async () => {
    const assistant1 = getFakeAssistant();
    const assistant2 = getFakeAssistant();

    assistantsStore.set({
      assistants: [assistant1, assistant2]
    });

    render(AssistantsManagementPage, { data: { assistants: [assistant1, assistant2] } });

    screen.getByText(assistant1.name!);
    screen.getByText(assistant2.name!);
  });
  // Assistant search tested with e2e
});
