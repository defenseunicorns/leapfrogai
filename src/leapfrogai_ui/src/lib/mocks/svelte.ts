import { type Readable, readable } from 'svelte/store';
import type { Navigation, Page } from '@sveltejs/kit';
import { fakeThreads } from '../../../testUtils/fakeData';
import { faker } from '@faker-js/faker';
import { getUnixSeconds } from '$helpers/dates';

type GetStoresOverrides = {
  url: string;
  params: Record<string, string>;
};

export const getStores = (
  options: GetStoresOverrides = { url: 'http://localhost', params: {} }
) => {
  const navigating = readable<Navigation | null>(null);
  const page = readable<Page>({
    url: new URL(options.url),
    params: options.params,
    route: { id: null },
    status: 200,
    error: null,
    // TODO - the profile and session types are incompletely mocked out
    data: {
      conversations: fakeThreads,
      profile: {},
      session: {
        user: {
          id: faker.string.uuid(),
          app_metadata: {},
          user_metadata: {},
          aud: '',
          created_at: new Date().toISOString()
        }
      }
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
