import { GET } from './+server';
import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../vitest-setup';
import { getFakeAssistant } from '$testUtils/fakeData';

describe('/api/assistants', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({
        locals: {
          safeGetSession: sessionNullMock
        }
      })
    ).rejects.toMatchObject({
      status: 401
    });
  });
  it('returns a list of assistants', async () => {
    const assistant1 = getFakeAssistant();
    const assistant2 = getFakeAssistant();
    mockOpenAI.setAssistants([assistant1, assistant2]);

    const res = await GET({
      locals: {
        safeGetSession: sessionMock
      }
    });
    expect(res.status).toEqual(200);
    const resJson = await res.json();

    expect(resJson).toEqual([assistant1, assistant2]);
  });
});
