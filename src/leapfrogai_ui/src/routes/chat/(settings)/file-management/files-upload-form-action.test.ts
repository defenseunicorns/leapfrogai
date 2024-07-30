import { actions } from './+page.server';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';

describe('the files upload form action', () => {
  // note - actual upload functionality is tested with a Playwright e2e test
  it('returns a 400 if the request data is invalid', async () => {
    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST'
    });

    const res = await actions.default({ request, locals: getLocalsMock() } as RequestEvent<
      RouteParams,
      '/chat/(settings)/file-management'
    >);
    expect(res?.status).toEqual(400);
  });
  it('returns a 401 if the request is unauthenticated', async () => {
    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST'
    });
    const res = await actions.default({
      request,
      locals: getLocalsMock({ nullSession: true })
    } as RequestEvent<RouteParams, '/chat/(settings)/file-management'>);

    expect(res?.status).toEqual(401);
  });
});
