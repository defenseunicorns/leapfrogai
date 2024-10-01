import { render, screen, within } from '@testing-library/svelte';
import { load } from './+page.server';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { newAPIKeySchema } from '$schemas/apiKey';
import ApiKeyPage from './+page.svelte';
import {
  mockCreateApiKeyFormAction,
  mockDeleteApiKey,
  mockGetKeys
} from '$lib/mocks/api-key-mocks';
import { type APIKeyRow, type APIKeysForm, PERMISSIONS } from '$lib/types/apiKeys';
import { fakeKeys } from '$testUtils/fakeData';
import userEvent from '@testing-library/user-event';
import { toastStore } from '$stores';
import { formatDate } from '$helpers/dates';
import { vi } from 'vitest';
import { faker } from '@faker-js/faker';
import { getLocalsMock } from '$lib/mocks/misc';
import stores from '$app/stores';

const { mockSvelteStores } = await vi.hoisted(() => import('$lib/mocks/svelte'));

// The DeleteApiKeyModal access $page.data so we re-mock it out here with the keys set to a static value we can
// use throughout the tests when mocking the server load data as well
vi.mock('$app/stores', async (): Promise<typeof stores> => {
  const { fakeThreads, fakeAssistants, fakeKeys } = await import('$testUtils/fakeData');
  return await mockSvelteStores({
    url: `http://localhost/chat/${fakeThreads[0].id}`,
    params: { thread_id: fakeThreads[0].id },
    data: {
      threads: fakeThreads,
      assistants: fakeAssistants,
      files: [],
      apiKeys: fakeKeys
    }
  });
});

describe('api keys', () => {
  let form: APIKeysForm;
  let searchbox: HTMLElement;

  beforeEach(async () => {
    mockGetKeys(fakeKeys);

    // @ts-expect-error: full mocking of load function params not necessary and is overcomplicated
    const data = await load({ depends: vi.fn(), locals: getLocalsMock() });
    form = await superValidate(yup(newAPIKeySchema));
    render(ApiKeyPage, {
      data: { ...data, form }
    });
    searchbox = screen.getByRole('textbox', {
      name: /search/i
    });
  });
  it('lists all the keys', () => {
    fakeKeys.forEach((key) => {
      expect(screen.getByText(key.name));
    });
  });
  it('searches by name', async () => {
    expect(screen.getByText(fakeKeys[1].name)).toBeInTheDocument();
    await userEvent.type(searchbox, fakeKeys[0].name);
    expect(screen.queryByText(fakeKeys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(fakeKeys[0].name)).toBeInTheDocument();
  });
  it('searches for keys by created date', async () => {
    expect(screen.getByText(fakeKeys[0].name)).toBeInTheDocument();
    await userEvent.type(searchbox, formatDate(new Date(fakeKeys[0].created_at * 1000)));
    expect(screen.queryByText(fakeKeys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(fakeKeys[0].name)).toBeInTheDocument();
  });
  it('searches for keys by expiration date', async () => {
    expect(screen.getByText(fakeKeys[0].name)).toBeInTheDocument();
    await userEvent.type(searchbox, formatDate(new Date(fakeKeys[0].expires_at * 1000)));
    expect(screen.queryByText(fakeKeys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(fakeKeys[0].name)).toBeInTheDocument();
  });
  it('searches for keys by secret', async () => {
    expect(screen.getByText(fakeKeys[0].name)).toBeInTheDocument();
    await userEvent.type(searchbox, fakeKeys[0].api_key.slice(-4));
    expect(screen.queryByText(fakeKeys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(fakeKeys[0].name)).toBeInTheDocument();
  });

  it('sorts by created_at by default', async () => {
    const keysSortedByCreatedAt = fakeKeys.sort((a, b) => a.created_at - b.created_at);
    const rows = screen.getAllByRole('row');
    // The first row is the header
    const rowKeyNames = rows.slice(1).map((row) => {
      // Get all the cells within the current row
      const cells = row.querySelectorAll('td');

      // Assuming created_at is in the last column or you know the specific index
      const createdAtCell = cells[0]; // name column is the first column
      return createdAtCell.textContent;
    });
    expect(rowKeyNames).toEqual(keysSortedByCreatedAt.map((key) => key.name));
  });
  // Only testing the "Name" column
  it('sorts by column', async () => {
    const keysSortedByName = fakeKeys.sort((a, b) => a.name.localeCompare(b.name));
    await userEvent.click(screen.getByText('Name'));
    const rows = screen.getAllByRole('row');
    // The first row is the header
    const rowKeyNames = rows.slice(1).map((row) => {
      // Get all the cells within the current row
      const cells = row.querySelectorAll('td');

      // Assuming created_at is in the last column or you know the specific index
      const createdAtCell = cells[0]; // name column is the first column
      return createdAtCell.textContent;
    });
    expect(rowKeyNames).toEqual(keysSortedByName.map((key) => key.name));
  });

  it('can delete keys', async () => {
    mockDeleteApiKey();
    const toastSpy = vi.spyOn(toastStore, 'addToast');

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await userEvent.click(checkbox);
    await userEvent.click(screen.getByRole('button', { name: /delete/i }));

    const modal = screen.getByTestId('delete-api-key-modal');
    expect(modal).toBeInTheDocument();
    screen.getByText(fakeKeys.map((key) => key.name).join(', '));
    await userEvent.click(within(modal).getByRole('button', { name: /delete/i }));

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'Keys Deleted'
    });
  });
  it('shows the create btn and not the actions btns when no items are selected', async () => {
    expect(screen.getByRole('button', { name: /create new/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /delete/i })).not.toBeInTheDocument();

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await userEvent.click(checkbox);

    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /create new/i })).not.toBeInTheDocument();
  });
  it('replaces the delete button with a disabled loading spinner button while deleting', async () => {
    mockDeleteApiKey({ withDelay: true });

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await userEvent.click(checkbox);
    const deleteBtn = screen.getByRole('button', { name: /delete/i });
    await userEvent.click(deleteBtn);
    const modal = screen.getByTestId('delete-api-key-modal');
    await userEvent.click(within(modal).getByRole('button', { name: /delete/i }));

    expect(deleteBtn).not.toBeInTheDocument();
    const deleteSpinnerBtn = screen.getByRole('button', { name: /deleting/i });
    expect(deleteSpinnerBtn).toBeInTheDocument();
    expect(deleteSpinnerBtn).toBeDisabled();
    screen.getByText('Deleting...');
  });

  // This test passes but is throwing a type error:
  // TypeError: Cannot read properties of undefined (reading '$set')
  // TODO - https://github.com/defenseunicorns/leapfrogai/issues/636
  it.skip('can create new keys', async () => {
    const toastSpy = vi.spyOn(toastStore, 'addToast');
    const keyName = faker.word.noun();
    const sixtyDays = new Date();
    sixtyDays.setDate(sixtyDays.getDate() + 60);
    const api_key_to_return = 'lfai_12345';
    const key: APIKeyRow = {
      id: faker.string.uuid(),
      name: keyName,
      api_key: api_key_to_return,
      created_at: new Date().getTime(),
      expires_at: sixtyDays.getTime(),
      permissions: PERMISSIONS.ALL
    };

    mockCreateApiKeyFormAction(key);

    await userEvent.click(screen.getByRole('button', { name: /create new/i }));
    const modal = screen.getByTestId('create-api-key-modal');
    await userEvent.type(within(modal).getByRole('textbox'), keyName);
    await userEvent.click(screen.getByText('60 Days'));

    await userEvent.click(within(modal).getByRole('button', { name: /create/i }));

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'Created Successfully',
      subtitle: `${key.name} created successfully.`
    });
  });

  // Note - not testing the feature flagging of blocking api-keys page when using OPEN AI
  // Note - testing copying of created key via E2E due to TypeError mentioned with above test
});
