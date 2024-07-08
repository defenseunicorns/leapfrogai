import { GET } from './+server';
import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../vitest-setup';
import { getFakeMessage } from '$testUtils/fakeData';

const url = new URL('http://localhost');

const message = getFakeMessage();

describe('/api/messages', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({
        url,
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
        url,
        locals: {
          safeGetSession: sessionMock
        }
      })
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a message', async () => {
    const myUrl = new URL(
      `http://localhost:5173?thread_id=${message.thread_id}&message_id=${message.id}`
    );
    mockOpenAI.setMessages([message]);

    const res = await GET({
      url: myUrl,
      locals: {
        safeGetSession: sessionMock
      }
    });
    expect(res.status).toEqual(200);
    const resJson = await res.json();

    expect(resJson).toEqual(message);
  });

  it('returns a 500 when there is an error getting a message', async () => {
    mockOpenAI.setError('retrieveMessage');
    const myUrl = new URL(
      `http://localhost:5173?thread_id=${message.thread_id}&message_id=${message.id}`
    );
    mockOpenAI.setMessages([message]);

    await expect(
      GET({
        url: myUrl,
        locals: { safeGetSession: sessionMock }
      })
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
