import { fireEvent, render, screen, waitFor, within } from '@testing-library/svelte';
import { load } from './+page.server';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { newAPIKeySchema } from '$schemas/apiKey';
import ApiKeyPage from './+page.svelte';
import {
  mockCreateApiKey,
  mockCreateApiKeyFormAction,
  mockDeleteApiKey,
  mockGetKeys
} from '$lib/mocks/api-key-mocks';
import type { APIKeysForm, NewApiKeyInput } from '$lib/types/apiKeys';
import { getFakeApiKeys } from '$testUtils/fakeData';
import userEvent from '@testing-library/user-event';
import { toastStore } from '$stores';
import { formatDate } from '$helpers/dates';
import { vi } from 'vitest';
import { faker } from '@faker-js/faker';
import { sessionMock } from '$lib/mocks/supabase-mocks';

describe('api keys', () => {
  let form: APIKeysForm;
  const keys = getFakeApiKeys();

  beforeEach(async () => {
    mockGetKeys(keys);
    const data = await load({ depends: vi.fn(), locals: { safeGetSession: sessionMock } });
    form = await superValidate(yup(newAPIKeySchema));
    render(ApiKeyPage, {
      data: { ...data, form }
    });
  });
  it('lists all the keys', () => {
    keys.forEach((key) => {
      expect(screen.getByText(key.name));
    });
  });
  it('searches by name', async () => {
    expect(screen.getByText(keys[1].name)).toBeInTheDocument();
    await userEvent.type(screen.getByRole('searchbox'), keys[0].name);
    expect(screen.queryByText(keys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
  });
  it('searches for keys by date', async () => {
    const currentDate = new Date();
    const yesterday = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth(),
      currentDate.getDate() - 1
    );

    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
    await userEvent.type(screen.getByRole('searchbox'), formatDate(new Date(keys[0].created_at)));
    expect(screen.queryByText(keys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
  });
  it('can delete keys', async () => {
    mockDeleteApiKey();
    const toastSpy = vi.spyOn(toastStore, 'addToast');

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await fireEvent.click(checkbox);

    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
    expect(screen.getByText(keys[1].name)).toBeInTheDocument();

    const deleteBtns = screen.getAllByRole('button', { name: /delete/i });

    await userEvent.click(deleteBtns[0]);

    screen.getByText(`Are you sure you want to delete ${keys[0].name}, ${keys[1].name}?`);
    await userEvent.click(deleteBtns[1]);

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'Keys Deleted',
      subtitle: ''
    });
  });
  it('disables the delete button when there are no rows selected', async () => {
    // Note - the delete button is hidden when there are no rows selected, but still on the page so it needs to be
    // disabled

    const deleteBtn = screen.getAllByRole('button', { name: /delete/i })[0];
    expect(deleteBtn).toBeDisabled();
  });
  it('replaces the delete button with a loading spinner while deleting', async () => {
    const deleteBtns = screen.getAllByRole('button', { name: /delete/i });

    const checkboxes = screen.getAllByRole('checkbox');

    await fireEvent.click(checkboxes[1]); // select key
    expect(screen.queryByTestId('delete-pending')).not.toBeInTheDocument(); // no loading spinner yet
    await userEvent.click(deleteBtns[0]);
    await waitFor(() => expect(deleteBtns[1]).not.toBeDisabled());
    // Deletion check completed
    screen.getByText(/are you sure you want to delete \?/i);

    await userEvent.click(deleteBtns[1]); // confirm delete
    const deleteBtns2 = screen.getAllByRole('button', { name: /delete/i });
    expect(deleteBtns2).toHaveLength(1); // only modal delete btn remains in document
    expect(screen.queryByTestId('delete-pending')).toBeInTheDocument();
  });
  // This may have to be an e2e
  it('can create new keys', async () => {
    const toastSpy = vi.spyOn(toastStore, 'addToast');

    const keyName = faker.word.noun();
    const sixtyDays = new Date();
    sixtyDays.setDate(sixtyDays.getDate() + 60);
    const api_key_to_return = 'lfai_12345';
    mockCreateApiKeyFormAction(keyName, api_key_to_return, sixtyDays.getTime());

    await userEvent.click(screen.getByRole('button', { name: /create new/i }));
    await userEvent.type(screen.getByLabelText(/name/i), keyName);
    await userEvent.click(screen.getByText('60 Days'));

    const dialog = screen.getByRole('dialog', {
      name: /create new api key/i
    });

    await userEvent.click(within(dialog).getByRole('button', { name: /create/i }));

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'API key created',
      subtitle: ''
    });
  });

  // Toasts?
  // TODO - test here for feature flag?
  // TODO - test copy key and disappear
});
