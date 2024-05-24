import { mockOpenAI } from '../../../../../vitest-setup';
import { getFakeThread } from '$testUtils/fakeData';
import { GET } from './+server';
import { sessionMock } from '$lib/mocks/supabase-mocks';

describe('/api/threads/[thread_id]', () => {
  it('returns a thread', async () => {
    const thread = getFakeThread();
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    mockOpenAI.setThread(thread);

    const res = await GET({
      request,
      params: {
        thread_id: thread.id
      },
      locals: {
        getSession: sessionMock
      }
    });

    const resData = await res.json();
    expect(res.status).toEqual(200);
    expect(resData).toEqual(thread);
  });
  it('returns a 500 if there is an error retrieving the thread', async () => {
    const thread = getFakeThread();

    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    mockOpenAI.setThread(thread);
    mockOpenAI.setError('retrieveThread');

    await expect(
      GET({
        request,
        params: {
          thread_id: thread.id
        },
        locals: {
          getSession: sessionMock
        }
      })
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
