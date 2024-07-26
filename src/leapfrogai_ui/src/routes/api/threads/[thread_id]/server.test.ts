import { mockOpenAI } from '../../../../../vitest-setup';
import { getFakeThread } from '$testUtils/fakeData';
import { GET } from './+server';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';

const request = new Request('http://thisurlhasnoeffect', {
  method: 'GET'
});

describe('/api/threads/[thread_id]', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/threads/[thread_id]'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when there is no thread_id param', async () => {
    await expect(
      GET({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/[thread_id]'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a thread', async () => {
    const thread = getFakeThread();
    mockOpenAI.setThreads([thread]);

    const res = await GET({
      request,
      params: {
        thread_id: thread.id
      },
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/threads/[thread_id]'>);

    const resData = await res.json();
    expect(res.status).toEqual(200);
    expect(resData).toEqual(thread);
  });
  it('returns a 500 if there is an error retrieving the thread', async () => {
    const thread = getFakeThread();

    mockOpenAI.setThreads([thread]);
    mockOpenAI.setError('listMessages');

    await expect(
      GET({
        request,
        params: {
          thread_id: thread.id
        },
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/[thread_id]'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
