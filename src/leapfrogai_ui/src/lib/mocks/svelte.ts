type GetStoresOverrides = {
  url?: string;
  params?: Record<string, string>;
  data?: object;
};

export const mockSvelteStores = async (options: GetStoresOverrides = {}) => {
  const { readable, writable } = await import('svelte/store');
  const { faker } = await import('@faker-js/faker');
  const { getFakeSession } = await import('$testUtils/fakeData');

  const { url = 'http://localhost', params = {}, data = {} } = options;

  const id = faker.string.uuid();
  const user_id = faker.string.uuid();
  const full_name = faker.person.fullName();
  const updated: typeof import('$app/stores').updated = {
    subscribe: readable(false).subscribe,
    check: () => Promise.resolve(false)
  };

  const getStores = () => ({
    navigating: readable(null),
    page: readable({
      url: new URL(url),
      params,
      route: { id: null },
      status: 200,
      error: null,
      data: {
        profile: { id, full_name: full_name, thread_ids: [] },
        session: getFakeSession({ user_id, full_name }),
        ...data
      },
      state: {},
      form: null
    }),
    session: writable(null),
    updated
  });

  const page: typeof import('$app/stores').page = {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    subscribe(fn: any) {
      return getStores().page.subscribe(fn);
    }
  };
  const navigating: typeof import('$app/stores').navigating = {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    subscribe(fn: any) {
      return getStores().navigating.subscribe(fn);
    }
  };

  return { getStores, page, navigating, updated };
};
