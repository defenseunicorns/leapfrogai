import { GET } from './+server';
import { mockOpenAI } from '../../../../vitest-setup';
import { getFakeFiles } from '$testUtils/fakeData';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../.svelte-kit/types/src/routes/api/threads/[thread_id]/$types';
import { getLocalsMock } from '$lib/mocks/misc';

describe('/api/files', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/files'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });
  it('returns a list of files', async () => {
    const files = getFakeFiles();

    mockOpenAI.setFiles(files);

    const res = await GET({
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/files'>);
    expect(res.status).toEqual(200);
    const resJson = await res.json();

    expect(resJson).toEqual(files);
  });
});
