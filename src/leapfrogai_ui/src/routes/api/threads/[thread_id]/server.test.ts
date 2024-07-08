import { mockOpenAI } from '../../../../../vitest-setup';
import { getFakeThread } from '$testUtils/fakeData';
import { GET } from './+server';
import { sessionMock } from '$lib/mocks/supabase-mocks';

describe('/api/threads/[thread_id]', () => {
  it('returns a thread', async () => {
    const thread = getFakeThread();
    mockOpenAI.setThreads([thread]);

    const res = await GET({
      params: {
        thread_id: thread.id
      },
      locals: {
        safeGetSession: sessionMock
      }
    });

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
        params: {
          thread_id: thread.id
        },
        locals: {
          safeGetSession: sessionMock
        }
      })
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
