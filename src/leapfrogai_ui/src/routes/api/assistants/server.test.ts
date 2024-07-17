import { GET } from './+server';
import { mockOpenAI } from '../../../../vitest-setup';
import { getFakeAssistant } from '$testUtils/fakeData';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../.svelte-kit/types/src/routes/api/messages/new/$types';

const request = new Request('http://thisurlhasnoeffect', {
  method: 'GET'
});

describe('/api/assistants', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/assistants'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });
  it('returns a list of assistants', async () => {
    const assistant1 = getFakeAssistant();
    const assistant2 = getFakeAssistant();
    mockOpenAI.setAssistants([assistant1, assistant2]);

    const res = await GET({
      request,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/assistants'>);
    expect(res.status).toEqual(200);
    const resJson = await res.json();

    expect(resJson).toEqual([assistant1, assistant2]);
  });
});
