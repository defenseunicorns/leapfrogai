import { GET } from './+server';
import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../vitest-setup';
import { getFakeFiles } from '$testUtils/fakeData';

describe('/api/files', () => {
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
  it('returns a list of files', async () => {
    const files = getFakeFiles();

    mockOpenAI.setFiles(files);

    const res = await GET({
      locals: {
        safeGetSession: sessionMock
      }
    });
    expect(res.status).toEqual(200);
    const resJson = await res.json();

    expect(resJson).toEqual(files);
  });
});
