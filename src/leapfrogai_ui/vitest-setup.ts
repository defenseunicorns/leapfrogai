import '@testing-library/jest-dom/vitest';
import '@testing-library/svelte/vitest';
import { setupServer } from 'msw/node';
import { afterAll, afterEach, beforeAll, vi } from 'vitest';
import * as environment from '$app/environment';
import * as navigation from '$app/navigation';
import * as stores from '$app/stores';
import { fakeAssistants, fakeThreads } from '$testUtils/fakeData';
import OpenAIMock from '$lib/mocks/openai';
import dotenv from 'dotenv';

dotenv.config();

//Calls to vi.mock are hoisted to the top of the file, so you don't have access to variables declared in the global file scope unless they are defined with vi.hoisted before the call.
const { getStores } = await vi.hoisted(() => import('$lib/mocks/svelte'));

// Fixes error: node.scrollIntoView is not a function
window.HTMLElement.prototype.scrollIntoView = function () {};

export const mockOpenAI = new OpenAIMock({ apiKey: '', baseURL: '' });

vi.doMock('$lib/server/constants', () => {
  return {
    getOpenAiClient: vi.fn().mockReturnValue(mockOpenAI)
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
  const page: typeof stores.page = {
    subscribe(fn) {
      return getStores({
        url: `http://localhost/chat/${fakeThreads[0].id}`,
        params: { thread_id: fakeThreads[0].id },
        data: {
          threads: fakeThreads,
          assistants: fakeAssistants,
          assistant: undefined,
          files: []
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

export const restHandlers = [];

export const server = setupServer(...restHandlers);

// Start server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));

//  Close server after all tests
afterAll(() => server.close());

// Reset handlers after each test `important for test isolation`
afterEach(() => server.resetHandlers());
