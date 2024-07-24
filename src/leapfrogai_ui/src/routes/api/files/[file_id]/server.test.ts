import { GET } from './+server';
import { mockOpenAI } from '../../../../../vitest-setup';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';

const request = new Request('http://thisurlhasnoeffect', {
  method: 'GET'
});

describe('/api/files/[file_id]', () => {
  it('returns a 401 when there is no session', async () => {
    await expect(
      GET({ request, params: {}, locals: getLocalsMock({ nullSession: true }) } as RequestEvent<
        RouteParams,
        '/api/files/[file_id]'
      >)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('should return 400 if file_id is missing', async () => {
    await expect(
      GET({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/[file_id]'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('request the file from the API', async () => {
    await GET({ request, params: { file_id: 'file_123' }, locals: getLocalsMock() } as RequestEvent<
      RouteParams,
      '/api/files/[file_id]'
    >);

    expect(mockOpenAI.files.content).toHaveBeenCalledTimes(1);
    expect(mockOpenAI.files.content).toHaveBeenCalledWith('file_123');
  });
});
