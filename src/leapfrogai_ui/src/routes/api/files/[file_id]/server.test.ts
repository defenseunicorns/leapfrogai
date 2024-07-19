import { GET } from './+server';
import { mockOpenAI } from '../../../../../vitest-setup';
import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';

describe('/api/files/[file_id]', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({
        params: { file_id: 'file_123' },
        locals: {
          safeGetSession: sessionNullMock
        }
      })
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('should return 400 if file_id is missing', async () => {
    await expect(
      GET({
        params: {},
        locals: {
          safeGetSession: sessionMock
        }
      })
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('request the file from the API', async () => {
    await GET({
      params: { file_id: 'file_123' },
      locals: {
        safeGetSession: sessionMock
      }
    });
    expect(mockOpenAI.files.content).toHaveBeenCalledTimes(1);
    expect(mockOpenAI.files.content).toHaveBeenCalledWith('file_123');
  });
});
