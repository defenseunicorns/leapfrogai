import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import NewAssistantPageWithToast from './NewAssistantPageWithToast.test.svelte';
import { afterAll, beforeAll, type MockInstance, vi } from 'vitest';
import * as navigation from '$app/navigation';
import { ASSISTANTS_DESCRIPTION_MAX_LENGTH, ASSISTANTS_NAME_MAX_LENGTH } from '$lib/constants';

describe('New Assistant page', () => {
  let goToSpy: MockInstance;

  beforeAll(() => {
    goToSpy = vi.spyOn(navigation, 'goto');
  });

  afterEach(() => {
    vi.clearAllMocks();
  });
  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('has a modal that navigates back to the management page', async () => {
    render(NewAssistantPageWithToast);

    const cancelBtn = screen.getAllByRole('button', { name: /cancel/i })[0];
    await userEvent.click(cancelBtn);

    await userEvent.click(screen.getByText('Leave this page'));

    expect(goToSpy).toHaveBeenCalledWith('/chat/assistants-management');
  });
  it('has a modal that stays on page when canceled', async () => {
    render(NewAssistantPageWithToast);

    const cancelBtn = screen.getAllByRole('button', { name: /cancel/i })[0];
    await userEvent.click(cancelBtn);

    await userEvent.click(screen.getByText('Stay on page'));

    expect(goToSpy).toHaveBeenCalledTimes(0);
  });

  it('limits the name input length', async () => {
    render(NewAssistantPageWithToast);
    const nameField = screen.getByRole('textbox', { name: /name/i });
    await userEvent.type(nameField, 'a'.repeat(ASSISTANTS_NAME_MAX_LENGTH + 1));
    expect(nameField).toHaveValue('a'.repeat(ASSISTANTS_NAME_MAX_LENGTH));
  });

  it('limits the description input length', async () => {
    render(NewAssistantPageWithToast);
    const descriptionField = screen.getByRole('textbox', { name: /description/i });
    await userEvent.type(descriptionField, 'a'.repeat(ASSISTANTS_DESCRIPTION_MAX_LENGTH + 1));
    expect(descriptionField).toHaveValue('a'.repeat(ASSISTANTS_DESCRIPTION_MAX_LENGTH));
  });
  /* Note - instructions length limit is too long, test times out.
     Attempts to mock the constant required specifying each variable from the constants file in the mock
     (vi.importActual) did not work
     The extra maintenance overhead was deemed not worth testing this field
  */
});
