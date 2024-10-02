import { GET } from './+server';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';
import {
  selectSingleReturnsMockError,
  supabaseFromMockWrapper,
  supabaseSelectSingleByIdMock
} from '$lib/mocks/supabase-mocks';
import { getFakeThread } from '$testUtils/fakeData';
import { mockOpenAI } from '../../../../vitest-setup';
import * as apiHelpers from '../helpers';

const request = new Request('http://thisurlhasnoeffect', {
  method: 'GET'
});

const thread1 = getFakeThread({ numMessages: 1 });
const thread2 = getFakeThread({ numMessages: 2 });
const fakeProfile = { thread_ids: [thread1.id, thread2.id] };

describe('/api/threads', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/threads'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });
  it("returns a user's threads", async () => {
    const thread1WithoutMessages = { ...thread1, messages: undefined };
    const thread2WithoutMessages = { ...thread2, messages: undefined };

    mockOpenAI.setThreads([thread1WithoutMessages, thread2WithoutMessages]);
    mockOpenAI.setMessages([...(thread1.messages || []), ...(thread2.messages || [])]);

    const res = await GET({
      request,
      locals: getLocalsMock({
        supabase: supabaseFromMockWrapper({
          ...supabaseSelectSingleByIdMock(fakeProfile)
        })
      })
    } as RequestEvent<RouteParams, '/api/threads'>);

    expect(res.status).toEqual(200);
    const resJson = await res.json();
    // Note - our fake threads already have messages attached, we are checking here that the
    // API fetched the messages and added them to the threads since real threads don't have messages
    expect(resJson[0].id).toEqual(thread1.id);
    expect(resJson[0].messages).toEqual(thread1.messages);
    expect(resJson[1].id).toEqual(thread2.id);
    expect(resJson[1].messages).toEqual(thread2.messages);
  });
  it('still returns threads that were successfully retrieved when there is an error getting a thread', async () => {
    mockOpenAI.setThreads([thread2]);
    mockOpenAI.setError('retrieveThread'); // fail the first thread fetching
    const res = await GET({
      request,
      locals: getLocalsMock({
        supabase: supabaseFromMockWrapper({
          ...supabaseSelectSingleByIdMock(fakeProfile)
        })
      })
    } as RequestEvent<RouteParams, '/api/threads'>);

    expect(res.status).toEqual(200);
    const resJson = await res.json();
    expect(resJson[0].id).toEqual(thread2.id);
  });
  it('still returns threads that were successfully retrieved when there is an error getting messages for a thread', async () => {
    mockOpenAI.setThreads([thread1, thread2]);
    mockOpenAI.setError('listMessages'); // fail the first thread's message fetching
    const res = await GET({
      request,
      locals: getLocalsMock({
        supabase: supabaseFromMockWrapper({
          ...supabaseSelectSingleByIdMock(fakeProfile)
        })
      })
    } as RequestEvent<RouteParams, '/api/threads'>);

    expect(res.status).toEqual(200);
    const resJson = await res.json();
    expect(resJson[0].id).toEqual(thread2.id);
  });
  it('returns an empty array if there is an unhandled error fetching threads', async () => {
    vi.spyOn(apiHelpers, 'getThreadWithMessages').mockImplementationOnce(() => {
      throw new Error('fake error');
    });
    const consoleSpy = vi.spyOn(console, 'error');

    const res = await GET({
      request,
      locals: getLocalsMock({
        supabase: supabaseFromMockWrapper({
          ...supabaseSelectSingleByIdMock(fakeProfile)
        })
      })
    } as RequestEvent<RouteParams, '/api/threads'>);

    expect(res.status).toEqual(200);
    const resJson = await res.json();
    expect(resJson).toEqual([]);
    // ensure we hit the correct catch block/error case with this test
    expect(consoleSpy).toHaveBeenCalledWith('Error fetching threads: Error: fake error');
  });
  it("returns a 500 is an error getting the user's profile", async () => {
    await expect(
      GET({
        request,
        locals: getLocalsMock({
          supabase: supabaseFromMockWrapper({
            ...selectSingleReturnsMockError()
          })
        })
      } as RequestEvent<RouteParams, '/api/threads'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
