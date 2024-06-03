import { afterAll, beforeAll, vi } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import stores from '$app/stores';
import { fakeThreads, getFakeMessage, getFakeProfile } from '$testUtils/fakeData';
import {
  mockChatCompletion,
  mockGetAssistants,
  mockNewMessage,
  mockNewThreadError
} from '$lib/mocks/chat-mocks';
import { load } from './+page.server';
import { mockOpenAI } from '../../../../../vitest-setup';
import {
  sessionMock,
  supabaseFromMockWrapper,
  supabaseSelectSingleByIdMock
} from '$lib/mocks/supabase-mocks';
import ChatPageWithToast from './ChatPageWithToast.test.svelte';
import type { PageData } from '../../../../../.svelte-kit/types/src/routes/chat/(dashboard)/[[thread_id]]/$types';

const { getStores } = await vi.hoisted(() => import('$lib/mocks/svelte'));

let data: PageData;
const question = 'What is AI?';

describe('when there is NO active thread selected', () => {
  beforeAll(() => {
    vi.mock('$env/dynamic/public', () => {
      return {
        env: {
          PUBLIC_MESSAGE_LENGTH_LIMIT: '100'
        }
      };
    });

    // set no active thread
    vi.mock('$app/stores', (): typeof stores => {
      const page: typeof stores.page = {
        subscribe(fn) {
          return getStores({
            url: `http://localhost/chat`,
            params: {}
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
  });

  beforeEach(async () => {
    const allMessages = fakeThreads.flatMap((thread) => thread.messages);
    mockGetAssistants();
    mockOpenAI.setThreads(fakeThreads);
    mockOpenAI.setMessages(allMessages);

    const fakeProfile = getFakeProfile({ thread_ids: fakeThreads.map((thread) => thread.id) });

    data = await load({
      fetch: global.fetch,
      locals: {
        supabase: supabaseFromMockWrapper(supabaseSelectSingleByIdMock(fakeProfile)),
        safeGetSession: sessionMock
      }
    });
  });

  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('displays an error message when there is an error saving the new thread', async () => {
    const fakeMessage = getFakeMessage({ content: question });
    mockChatCompletion();
    mockNewThreadError();
    mockNewMessage(fakeMessage);

    const { getByLabelText } = render(ChatPageWithToast, { data });

    const input = getByLabelText('message input') as HTMLInputElement;
    const submitBtn = getByLabelText('send');

    await userEvent.type(input, question);
    await userEvent.click(submitBtn);
    await screen.findAllByText('Error saving thread.');
  });
});
