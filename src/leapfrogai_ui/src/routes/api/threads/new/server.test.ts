import { faker } from '@faker-js/faker';
import { POST } from './+server';
import { MAX_LABEL_SIZE } from '$lib/constants';
import { getFakeThread } from '$testUtils/fakeData';
import {
  selectSingleReturnsMockError,
  supabaseFromMockWrapper,
  supabaseInsertMock,
  supabaseSelectSingleByIdMock,
  supabaseUpdateErrorMock,
  updateSingleReturnsMock
} from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../../vitest-setup';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../../.svelte-kit/types/src/routes/api/messages/new/$types';

const thread = getFakeThread();
const validLabel = faker.string.alpha({ length: MAX_LABEL_SIZE - 1 });
const invalidLongLabel = faker.string.alpha({ length: MAX_LABEL_SIZE + 1 });
const fakeProfile = { thread_ids: ['thread_1'] };

describe('/api/threads/new', () => {
  it('returns a 200 when successful and updates the users profile with the new thread id', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: thread.metadata.label })
    });

    mockOpenAI.setTempThread(thread);

    const updateMock = updateSingleReturnsMock();

    const res = await POST({
      request,
      locals: getLocalsMock({
        supabase: supabaseFromMockWrapper({
          ...supabaseSelectSingleByIdMock(fakeProfile),
          ...updateMock
        })
      })
    } as RequestEvent<RouteParams, '/api/threads/new'>);

    const resData = await res.json();
    expect(res.status).toEqual(200);
    expect(resData).toEqual(thread);

    const updateCallArgs = updateMock.update.mock.calls[0];
    // @ts-expect-error: confirmed updateCallArgs is array and test is behaving properly
    expect(updateCallArgs[0]!.thread_ids).toHaveLength(2);
  });

  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: validLabel })
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when label is too long', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: invalidLongLabel })
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock({ supabase: supabaseInsertMock([thread]) })
      } as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when label is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock({ supabase: supabaseInsertMock([thread]) })
      } as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when extra body arguments are passed', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: validLabel, wrong: 'key' })
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock({ supabase: supabaseInsertMock([thread]) })
      } as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 500 when there is a supabase error updating the users profile', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: thread.metadata.label })
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock({
          supabase: supabaseFromMockWrapper({
            ...supabaseSelectSingleByIdMock(fakeProfile),
            ...supabaseUpdateErrorMock()
          })
        })
      } as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
  it('returns a 500 when there is a supabase error getting the users profile', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: thread.metadata.label })
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock({
          supabase: supabaseFromMockWrapper({
            ...supabaseSelectSingleByIdMock(fakeProfile),
            ...selectSingleReturnsMockError()
          })
        })
      } as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
  it('returns a 500 when there is an openai error', async () => {
    mockOpenAI.setError('createThread');
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: thread.metadata.label })
    });
    await expect(
      POST({
        request,
        locals: getLocalsMock({
          supabase: supabaseFromMockWrapper({
            ...supabaseSelectSingleByIdMock(fakeProfile),
            ...updateSingleReturnsMock()
          })
        })
      } as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
