import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';
import { getFakeMessage } from '$testUtils/fakeData';
import { POST } from './+server';
import { mockOpenAI } from '../../../../../vitest-setup';
import type { NewMessageInput } from '$lib/types/messages';
import { getMessageText } from '$helpers/threads';

const message = getFakeMessage({});

const validMessageBody: NewMessageInput = {
  content: getMessageText(message),
  thread_id: message.thread_id,
  role: message.role
};

describe('/api/messages/new', () => {
  it('returns a 200 when successful', async () => {
    mockOpenAI.setMessage(message);

    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify(validMessageBody)
    });

    const res = await POST({
      request,
      locals: { safeGetSession: sessionMock }
    });

    const resData = await res.json();
    expect(res.status).toEqual(200);
    expect(resData).toEqual(message);
  });

  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify(validMessageBody)
    });

    await expect(
      POST({
        request,
        locals: { safeGetSession: sessionNullMock }
      })
    ).rejects.toMatchObject({
      status: 401
    });
  });
  it('returns a 400 when the body is invalid', async () => {
    // Empty body
    let request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    await expect(
      POST({
        request,
        locals: { safeGetSession: sessionMock }
      })
    ).rejects.toMatchObject({
      status: 400
    });

    // Invalid param
    request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ ...validMessageBody, id: '123' })
    });

    await expect(
      POST({
        request,
        locals: { safeGetSession: sessionMock }
      })
    ).rejects.toMatchObject({
      status: 400
    });

    // Extra param
    request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ ...validMessageBody, break: 'me' })
    });

    await expect(
      POST({
        request,
        locals: { safeGetSession: sessionMock }
      })
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 500 when there is a openai error', async () => {
    mockOpenAI.setError('createMessage');
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify(validMessageBody)
    });

    await expect(
      POST({
        request,
        locals: { safeGetSession: sessionMock }
      })
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
