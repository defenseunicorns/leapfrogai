import { faker } from '@faker-js/faker';
import { DELETE } from './+server';
import {
  sessionMock,
  sessionNullMock,
  storageRemoveMock,
  supabaseStorageMockWrapper
} from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../../vitest-setup';

describe('/api/assistants/delete', () => {
  it('returns a 204 when the request completes and deletes the assistant avatar', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: faker.string.uuid() })
    });
    const storageMock = supabaseStorageMockWrapper(storageRemoveMock());

    const res = await DELETE({
      request,
      locals: { safeGetSession: sessionMock, supabase: storageMock }
    });
    expect(res.status).toEqual(204);

    expect(storageMock.storage.from.mock.calls[0]).toEqual(['assistant_avatars']);
  });
  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: faker.string.uuid() })
    });

    await expect(
      DELETE({
        request,
        locals: {
          safeGetSession: sessionNullMock,
          supabase: supabaseStorageMockWrapper(storageRemoveMock())
        }
      })
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when message ID is not a string', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: 123 })
    });

    await expect(
      DELETE({
        request,
        locals: {
          safeGetSession: sessionMock,
          supabase: supabaseStorageMockWrapper(storageRemoveMock())
        }
      })
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when message ID is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE'
    });

    await expect(
      DELETE({
        request,
        locals: {
          safeGetSession: sessionMock,
          supabase: supabaseStorageMockWrapper(storageRemoveMock())
        }
      })
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when extra body arguments are passed', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({
        id: faker.string.uuid(),
        wrong: 'key'
      })
    });
    await expect(
      DELETE({
        request,
        locals: {
          safeGetSession: sessionMock,
          supabase: supabaseStorageMockWrapper(storageRemoveMock())
        }
      })
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 500 when there is a openai error', async () => {
    mockOpenAI.setError('deleteAssistant');
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'DELETE',
      body: JSON.stringify({ id: faker.string.uuid() })
    });

    await expect(
      DELETE({
        request,
        locals: {
          safeGetSession: sessionMock,
          supabase: supabaseStorageMockWrapper(storageRemoveMock())
        }
      })
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
