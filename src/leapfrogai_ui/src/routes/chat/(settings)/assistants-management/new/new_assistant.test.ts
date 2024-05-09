import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { mockAssistantCreation, mockNewAssistantError } from '$lib/mocks/assistant-mocks';
import { getFakeNewAssistantInput } from '../../../../../../testUtils/fakeData';
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
  it('creates a new assistant', async () => {
    const newAssistantInput = getFakeNewAssistantInput();

    mockAssistantCreation(newAssistantInput);
    render(NewAssistantPageWithToast);

    const nameField = screen.getByRole('textbox', { name: /name/i });
    const taglineField = screen.getByRole('textbox', { name: /description/i });
    const instructionsField = screen.getByPlaceholderText(/you'll act as\.\.\./i);
    const saveBtn = screen.getByRole('button', { name: /save/i });

    await userEvent.type(nameField, newAssistantInput.name);
    await userEvent.type(taglineField, newAssistantInput.description);
    await userEvent.type(instructionsField, newAssistantInput.instructions);

    // Note - unknown how to change slider value so leaving at default

    await userEvent.click(saveBtn);
    await screen.findByText('Assistant Created.');
  });
  it('displays an error toast when there is an error creating an assistant', async () => {
    const newAssistantInput = getFakeNewAssistantInput();

    mockNewAssistantError();
    render(NewAssistantPageWithToast);

    const nameField = screen.getByRole('textbox', { name: /name/i });
    const taglineField = screen.getByRole('textbox', { name: /description/i });
    const instructionsField = screen.getByPlaceholderText(/you'll act as\.\.\./i);
    const saveBtn = screen.getByRole('button', { name: /save/i });

    await userEvent.type(nameField, newAssistantInput.name);
    await userEvent.type(taglineField, newAssistantInput.description);
    await userEvent.type(instructionsField, newAssistantInput.instructions);

    await userEvent.click(saveBtn);
    await screen.findByText('Error creating assistant.');
  });
  it('validates required fields', async () => {
    const newAssistantInput = getFakeNewAssistantInput();

    mockAssistantCreation(newAssistantInput);
    render(NewAssistantPageWithToast);

    const nameField = screen.getByRole('textbox', { name: /name/i });
    const taglineField = screen.getByRole('textbox', { name: /description/i });
    const instructionsField = screen.getByPlaceholderText(/you'll act as\.\.\./i);
    const saveBtn = screen.getByRole('button', { name: /save/i });

    await userEvent.type(nameField, newAssistantInput.name);

    await userEvent.click(saveBtn);

    expect(saveBtn).toHaveProperty('disabled', true);
    const requiredWarnings = screen.getAllByText(/Required/i);
    expect(requiredWarnings).toHaveLength(2);

    // Fill out remaining fields, ensure submit button remains disabled until form is valid
    await userEvent.type(taglineField, newAssistantInput.description);
    expect(saveBtn).toHaveProperty('disabled', true);
    await userEvent.type(instructionsField, newAssistantInput.instructions);
    expect(saveBtn).toHaveProperty('disabled', false);
  });
  it('has a modal that navigates back to the management page', async () => {
    render(NewAssistantPageWithToast);

    const cancelBtn = screen.getByRole('button', { name: /cancel/i });
    await userEvent.click(cancelBtn);

    await userEvent.click(screen.getByText('Leave this page'));

    expect(goToSpy).toHaveBeenCalledWith('/chat/assistants-management');
  });
  it('has a modal that stays on page when canceled', async () => {
    render(NewAssistantPageWithToast);

    const cancelBtn = screen.getByRole('button', { name: /cancel/i });
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
