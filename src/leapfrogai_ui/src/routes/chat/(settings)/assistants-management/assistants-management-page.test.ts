import { render, screen } from '@testing-library/svelte';
import AssistantsManagementPage from './+page.svelte';
import { getFakeAssistant, getFakeSession } from '$testUtils/fakeData';
import type { SupabaseClient } from '@supabase/supabase-js';

describe('Assistants management page', () => {
  // Assistant search tested with e2e

  it('displays all the assistants', async () => {
    const assistant1 = getFakeAssistant();
    const assistant2 = getFakeAssistant();

    render(AssistantsManagementPage, {
      data: {
        assistants: [assistant1, assistant2],
        session: getFakeSession(),
        title: 'Fake title',
        supabase: {} as unknown as SupabaseClient
      }
    });

    screen.getByTestId(`assistant-card-${assistant1.name!}`);
    screen.getByTestId(`assistant-card-${assistant2.name!}`);
  });
});
