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
import { fakeAssistants, fakeThreads, getFakeApiKeys } from '$testUtils/fakeData';
import userEvent from '@testing-library/user-event';
import { toastStore } from '$stores';
import { formatDate } from '$helpers/dates';
import { vi } from 'vitest';
import { faker } from '@faker-js/faker';
import { getLocalsMock } from '$lib/mocks/misc';
import stores from '$app/stores';

const { getStores } = await vi.hoisted(() => import('$lib/mocks/svelte'));
const keys = getFakeApiKeys({ numKeys: 4 });

// The DeleteApiKeyModal access $page.data so we re-mock it out here with the keys set to a static value we can
// use throughout the tests when mocking the server load data as well
vi.mock('$app/stores', (): typeof stores => {
  const page: typeof stores.page = {
    subscribe(fn) {
      return getStores({
        url: `http://localhost/chat/${fakeThreads[0].id}`,
        params: { thread_id: fakeThreads[0].id },
        data: {
          threads: fakeThreads,
          assistants: fakeAssistants,
          assistant: undefined,
          files: [],
          keys
        }
      }).page.subscribe(fn);
    }
  };
  const navigating: typeof stores.navigating = {
    subscribe(fn) {
      return getStores().navigating.subscribe(fn);
    }
  };
  const updated: typeof stores.updated = {
    subscribe(fn) {
      return getStores().updated.subscribe(fn);
    },
    check: () => Promise.resolve(false)
  };

  return {
    getStores,
    navigating,
    page,
    updated
  };
});

describe('api keys', () => {
  let form: APIKeysForm;

  let searchbox: HTMLElement;

  beforeEach(async () => {
    mockGetKeys(keys);
    keys[0].permissions = PERMISSIONS.ALL;
    keys[1].permissions = PERMISSIONS.READ;
    keys[2].permissions = PERMISSIONS.WRITE;
    keys[3].permissions = PERMISSIONS.READ_WRITE;

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
    keys.forEach((key) => {
      expect(screen.getByText(key.name));
    });
  });
  it('searches by name', async () => {
    expect(screen.getByText(keys[1].name)).toBeInTheDocument();
    await userEvent.type(searchbox, keys[0].name);
    expect(screen.queryByText(keys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
  });
  it('searches for keys by created date', async () => {
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
    await userEvent.type(searchbox, formatDate(new Date(keys[0].created_at * 1000)));
    expect(screen.queryByText(keys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
  });
  it('searches for keys by expiration date', async () => {
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
    await userEvent.type(searchbox, formatDate(new Date(keys[0].expires_at * 1000)));
    expect(screen.queryByText(keys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
  });
  it('searches for keys by secret', async () => {
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
    await userEvent.type(searchbox, keys[0].api_key.slice(-4));
    expect(screen.queryByText(keys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
  });
  it('searches for keys by permissions', async () => {
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
    await userEvent.type(searchbox, keys[0].permissions);
    expect(screen.queryByText(keys[1].name)).not.toBeInTheDocument();
    expect(screen.getByText(keys[0].name)).toBeInTheDocument();
  });

  it('can delete keys', async () => {
    mockDeleteApiKey();
    const toastSpy = vi.spyOn(toastStore, 'addToast');

    const actionsMenu = screen.getByRole('button', { name: /actions/i });
    await userEvent.click(actionsMenu);
    await userEvent.click(screen.getByRole('button', { name: /edit/i }));

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await userEvent.click(checkbox);
    await userEvent.click(screen.getByRole('button', { name: /delete/i }));

    const modal = screen.getByTestId('delete-api-key-modal');
    expect(modal).toBeInTheDocument();
    screen.getByText(keys.map((key) => key.name).join(', '));
    await userEvent.click(within(modal).getByRole('button', { name: /delete/i }));

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'Keys Deleted'
    });
  });
  it('disables the delete button when there are no rows selected', async () => {
    const actionsMenu = screen.getByRole('button', { name: /actions/i });
    await userEvent.click(actionsMenu);
    await userEvent.click(screen.getByRole('button', { name: /edit/i }));
    const deleteBtn = screen.getByRole('button', { name: /delete/i });
    expect(deleteBtn).toBeDisabled();
  });
  it('replaces the delete button with a disabled loading spinner button while deleting', async () => {
    mockDeleteApiKey({ withDelay: true });

    const actionsMenu = screen.getByRole('button', { name: /actions/i });
    await userEvent.click(actionsMenu);
    await userEvent.click(screen.getByRole('button', { name: /edit/i }));
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
