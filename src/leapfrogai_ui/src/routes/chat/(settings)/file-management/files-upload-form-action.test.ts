import { actions } from './+page.server';
import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';

describe('the files upload form action', () => {
  // note - actual upload functionality is tested with a Playwright e2e test
  it('returns a 400 if the request data is invalid', async () => {
    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST'
    });

    const res = await actions.default({ request, locals: { safeGetSession: sessionMock } });
    expect(res?.status).toEqual(400);
  });
  it('returns a 401 if the request is unauthenticated', async () => {
    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST'
    });
    const res = await actions.default({
      request,
      locals: { safeGetSession: sessionNullMock }
    });

    expect(res?.status).toEqual(401);
  });
});
