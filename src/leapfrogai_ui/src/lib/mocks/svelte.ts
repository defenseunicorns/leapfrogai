import { type Readable, readable } from 'svelte/store';
import type { Navigation, Page } from '@sveltejs/kit';
import { fakeThreads } from '$testUtils/fakeData';
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
  const navigating = readable<Navigation | null>(null);
  const page = readable<Page>({
    url: new URL(options.url),
    params: options.params,
    route: { id: null },
    status: 200,
    error: null,
    data: {
      threads: fakeThreads,
      profile: { id, full_name: 'fake user', thread_ids: [] },
      session: {
        access_token: '',
        refresh_token: '',
        expires_in: 3600,
        token_type: '',
        user: {
          id,
          app_metadata: {},
          user_metadata: {},
          aud: '',
          created_at: new Date().toISOString()
        }
      },
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
