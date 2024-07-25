import { faker } from '@faker-js/faker';
import { MAX_LABEL_SIZE } from '$lib/constants';
import { PUT } from './+server';
import { mockOpenAI } from '../../../../../../vitest-setup';
import { getFakeThread } from '$testUtils/fakeData';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../../../.svelte-kit/types/src/routes/api/messages/new/$types';

const validLabel = faker.string.alpha({ length: MAX_LABEL_SIZE - 1 });
const invalidLongLabel = faker.string.alpha({ length: MAX_LABEL_SIZE + 1 });

describe('/api/threads/update/label', () => {
  it('returns the updated thread when successful', async () => {
    const fakeThread = getFakeThread();
    mockOpenAI.setThreads([fakeThread]);

    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ id: fakeThread.id, label: validLabel })
    });
    const res = await PUT({
      request,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/threads/update/label'>);

    const updatedThread = await res.json();

    expect(res.status).toEqual(200);
    expect(updatedThread).toEqual({
      ...fakeThread,
      metadata: { ...fakeThread.metadata, label: validLabel }
    });
  });

  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'PUT',
      body: JSON.stringify({ id: faker.string.uuid(), label: validLabel })
    });

    await expect(
      PUT({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/threads/update/label'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when id is not a string', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'PUT',
      body: JSON.stringify({ id: 123, label: validLabel })
    });

    await expect(
      PUT({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/update/label'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 400 when id is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'PUT',
      body: JSON.stringify({ label: validLabel })
    });

    await expect(
      PUT({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/update/label'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 400 when the label is too long', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'PUT',
      body: JSON.stringify({ id: faker.string.uuid(), label: invalidLongLabel })
    });

    await expect(
      PUT({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/update/label'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when the label is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'PUT',
      body: JSON.stringify({ id: faker.string.uuid() })
    });

    await expect(
      PUT({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/update/label'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when extra body parameters are passed', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'PUT',
      body: JSON.stringify({ id: faker.string.uuid(), label: validLabel, break: 'me' })
    });

    await expect(
      PUT({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/update/label'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 500 when there is a openai error', async () => {
    mockOpenAI.setError('updateThread');

    const request = new Request('http://thisurlhasnoeffect', {
      method: 'PUT',
      body: JSON.stringify({ id: faker.string.uuid(), label: validLabel })
    });

    await expect(
      PUT({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/update/label'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
