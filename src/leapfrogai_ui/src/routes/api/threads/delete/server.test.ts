import { faker } from '@faker-js/faker';
import { DELETE } from './+server';
import {
  supabaseFromMockWrapper,
  supabaseSelectSingleByIdMock,
  supabaseUpdateErrorMock,
  updateSingleReturnsMock
} from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../../vitest-setup';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../../.svelte-kit/types/src/routes/api/messages/new/$types';
import type { Profile } from '$lib/types/profile';

const fakeProfile: Profile = { id: '123', full_name: 'fake name', thread_ids: ['thread_1'] };

describe('/api/threads/delete', () => {
  it('returns a 204 when the request completes and removes the id from the users profile', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: fakeProfile.thread_ids[0] })
    });

    const updateMock = updateSingleReturnsMock();

    const res = await DELETE({
      request,
      locals: getLocalsMock({
        supabase: supabaseFromMockWrapper({
          ...supabaseSelectSingleByIdMock(fakeProfile),
          ...updateMock
        })
      })
    } as RequestEvent<RouteParams, '/api/threads/delete'>);

    expect(res.status).toEqual(204);

    const updateCallArgs = updateMock.update.mock.calls[0] as unknown as [{ thread_ids: string[] }];

    expect(updateCallArgs[0]!.thread_ids).toHaveLength(0);
  });
  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: faker.string.uuid() })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock({
          nullSession: true
        })
      } as RequestEvent<RouteParams, '/api/threads/delete'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when thread ID is not a string', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: 123 })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/delete'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when thread ID is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE'
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/delete'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when extra body arguments are passed', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: faker.string.uuid(), wrong: 'key' })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/threads/delete'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 500 when there is a supabase error', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: faker.string.uuid() })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock({
          supabase: supabaseFromMockWrapper({
            ...supabaseSelectSingleByIdMock(fakeProfile),
            ...supabaseUpdateErrorMock()
          })
        })
      } as RequestEvent<RouteParams, '/api/threads/delete'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
  it('returns a 500 when there is a openai error', async () => {
    mockOpenAI.setError('deleteThread');
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: faker.string.uuid() })
    });

    await expect(
      DELETE({
        request,
        locals: getLocalsMock({
          supabase: supabaseFromMockWrapper({
            ...supabaseSelectSingleByIdMock(fakeProfile),
            ...updateSingleReturnsMock()
          })
        })
      } as RequestEvent<RouteParams, '/api/threads/delete'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
