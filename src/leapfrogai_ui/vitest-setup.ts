import '@testing-library/jest-dom/vitest';
import '@testing-library/svelte/vitest';
import { setupServer } from 'msw/node';
import type { Navigation, Page } from '@sveltejs/kit';
import { faker } from '@faker-js/faker';
import { readable, type Readable } from 'svelte/store';
import { afterAll, afterEach, beforeAll, vi } from 'vitest';
import * as environment from '$app/environment';
import * as navigation from '$app/navigation';
import * as stores from '$app/stores';
import { getFakeProfile, getFakeSession } from '$testUtils/fakeData';
import OpenAIMock from '$lib/mocks/openai';

// Fixes error: node.scrollIntoView is not a function
window.HTMLElement.prototype.scrollIntoView = function () {};

export const mockOpenAI = new OpenAIMock({ apiKey: '', baseURL: '' });

vi.doMock('$lib/server/constants', () => {
  return {
    openai: mockOpenAI
  };
});

vi.mock('$env/dynamic/public', () => {
  return {
    env: {
      PUBLIC_MESSAGE_LENGTH_LIMIT: '10000'
    }
  };
});

// Mock SvelteKit runtime module $app/environment
vi.mock('$app/environment', (): typeof environment => ({
  browser: false,
  dev: true,
  building: false,
  version: 'any'
}));

// Mock SvelteKit runtime module $app/navigation
vi.mock('$app/navigation', (): typeof navigation => ({
  afterNavigate: () => {},
  beforeNavigate: () => {},
  disableScrollHandling: () => {},
  goto: () => Promise.resolve(),
  invalidate: () => Promise.resolve(),
  invalidateAll: () => Promise.resolve(),
  preloadData: () => Promise.resolve({ type: 'loaded', status: 200, data: {} }),
  preloadCode: () => Promise.resolve(),
  onNavigate: () => {},
  pushState: () => {},
  replaceState: () => {}
}));

// Mock SvelteKit runtime module $app/stores
vi.mock('$app/stores', (): typeof stores => {
  const getStores: typeof stores.getStores = () => {
    const user_id = faker.string.uuid();
    const full_name = faker.person.fullName();
    const navigating = readable<Navigation | null>(null);
    const page = readable<Page>({
      url: new URL('http://localhost'),
      params: {},
      route: { id: null },
      status: 200,
      error: null,
      data: {
        threads: [],
        profile: getFakeProfile({ id: user_id, full_name }),
        session: getFakeSession({ user_id, full_name })
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

  const page: typeof stores.page = {
    subscribe(fn) {
      return getStores().page.subscribe(fn);
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

export const restHandlers = [];

export const server = setupServer(...restHandlers);

// Start server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));

//  Close server after all tests
afterAll(() => server.close());

// Reset handlers after each test `important for test isolation`
afterEach(() => server.resetHandlers());
