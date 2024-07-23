import { faker } from '@faker-js/faker';
import { DELETE } from './+server';
import { mockRevokeApiKey, mockRevokeApiKeyError } from '$lib/mocks/api-key-mocks';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../../.svelte-kit/types/src/routes/api/messages/new/$types';

describe('/api/api-keys/delete', () => {
  beforeEach(() => {
    mockRevokeApiKey();
  });
  it('returns a 204 when the request completes', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: [faker.string.uuid(), faker.string.uuid()] })
    });
    const res = await DELETE({
      request,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/api-keys/delete'>);
    expect(res.status).toEqual(204);
  });
  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: [faker.string.uuid(), faker.string.uuid()] })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/api-keys/delete'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when ids are not strings', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: [1, 2] })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/api-keys/delete'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns 400 when ids are missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({})
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/api-keys/delete'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 400 when extra body arguments are passed', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({
        ids: [],
        wrong: 'key'
      })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/api-keys/delete'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 500 when there is an API error', async () => {
    mockRevokeApiKeyError();
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ ids: [faker.string.uuid()] })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/api-keys/delete'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
