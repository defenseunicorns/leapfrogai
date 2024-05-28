import { faker } from '@faker-js/faker';
import { DELETE } from './+server';
import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../../vitest-setup';

describe('/api/files/delete', () => {
  it('returns a 204 when the request completes', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: ['1', '2'] })
    });

    const res = await DELETE({
      request,
      locals: {
        safeGetSession: sessionMock
      }
    });

    expect(res.status).toEqual(204);
  });
  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: faker.string.uuid() })
    });

    await expect(
      DELETE({
        request,
        locals: { safeGetSession: sessionNullMock }
      })
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when thread IDs is not a string array', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: 123 })
    });

    await expect(
      DELETE({ request, locals: { safeGetSession: sessionMock } })
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when thread IDs is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE'
    });

    await expect(
      DELETE({ request, locals: { safeGetSession: sessionMock } })
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when extra body arguments are passed', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: [faker.string.uuid()], wrong: 'key' })
    });

    await expect(
      DELETE({ request, locals: { safeGetSession: sessionMock } })
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 500 when there is a openai error', async () => {
    mockOpenAI.setError('deleteFile');
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: [faker.string.uuid()] })
    });

    await expect(
      DELETE({
        request,
        locals: {
          safeGetSession: sessionMock
        }
      })
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
