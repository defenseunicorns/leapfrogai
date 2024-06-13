import { GET } from './+server';
import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';

import { fakeThreads, getFakeMessage } from '$testUtils/fakeData';
import { mockOpenAI } from '../../../../../vitest-setup';

const message = getFakeMessage();

describe('/api/messages/[thread_id]', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({
        params: { thread_id: 'thread_123' },
        locals: {
          safeGetSession: sessionNullMock
        }
      })
    ).rejects.toMatchObject({
      status: 401
    });
  });
  it('should return 400 if thread_id or message_id is missing', async () => {
    await expect(
      GET({
        params: {},
        locals: {
          safeGetSession: sessionMock
        }
      })
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a list of messages for a thread', async () => {
    mockOpenAI.setThreads(fakeThreads);
    mockOpenAI.setMessages(fakeThreads[0].messages!);

    const res = await GET({
      params: { thread_id: fakeThreads[0].id },
      locals: {
        safeGetSession: sessionMock
      }
    });
    expect(res.status).toEqual(200);
    const resJson = await res.json();

    expect(resJson).toEqual(fakeThreads[0].messages);
  });

  it('returns a 500 when there is an error listing messages', async () => {
    mockOpenAI.setError('listMessages');

    mockOpenAI.setMessages([message]);

    await expect(
      GET({
        params: { thread_id: fakeThreads[0].id },
        locals: { safeGetSession: sessionMock }
      })
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
