import { faker } from '@faker-js/faker';
import { DELETE } from './+server';
import { mockOpenAI } from '../../../../../vitest-setup';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../../.svelte-kit/types/src/routes/api/messages/new/$types';
import { getLocalsMock } from '$lib/mocks/misc';

describe('/api/files/delete', () => {
  it('returns a 204 when the request completes', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: ['1', '2'] })
    });

    const res = await DELETE({
      request,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/files/delete'>);

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
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/files/delete'>)
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
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when thread IDs is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE'
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete'>)
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
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete'>)
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
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
