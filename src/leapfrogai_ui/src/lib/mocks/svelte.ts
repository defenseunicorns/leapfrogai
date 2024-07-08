import { type Readable, readable } from 'svelte/store';
import type { Navigation, Page } from '@sveltejs/kit';
import { getFakeSession } from '$testUtils/fakeData';
import { faker } from '@faker-js/faker';

type GetStoresOverrides = {
  url: string;
  params: Record<string, string>;
  data?: object;
};

export const getStores = (
  options: GetStoresOverrides = { url: 'http://localhost', params: {}, data: {} }
) => {
  const id = faker.string.uuid();
  const user_id = faker.string.uuid();
  const full_name = faker.person.fullName();
  const navigating = readable<Navigation | null>(null);

  const page = readable<Page>({
    url: new URL(options.url),
    params: options.params,
    route: { id: null },
    status: 200,
    error: null,
    data: {
      profile: { id, full_name: full_name, thread_ids: [] },
      session: getFakeSession({ user_id, full_name }),
      ...options.data
    },
    state: {},
    form: null
  });
  const updated: Readable<boolean> & { check(): Promise<boolean> } = {
    subscribe: readable(false).subscribe,
    check: () => Promise.resolve(false)
  };

  return { navigating, page, updated };
};
