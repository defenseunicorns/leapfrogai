import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';
import { POST } from './+server';
import { mockOpenAI } from '../../../../../vitest-setup';
import { requestWithFormData } from '$helpers/apiHelpers';
import * as constants from '$constants';

// Allows mocking important constants and only overriding values for specific tests
vi.mock('$constants', async () => {
  const actualConstants = await vi.importActual<typeof import('$constants')>('$constants');
  return {
    ...actualConstants
  };
});

describe('/api/audio/transcription', () => {
  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    await expect(
      POST({
        request,
        params: {},
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/audio/transcription'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('should return 400 if the form data is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', { method: 'POST' });
    await expect(
      POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/audio/transcription'
      >)
    ).rejects.toMatchObject({ status: 400 });
  });

  it('should return 400 if the file is missing from the form data', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: new FormData()
    });

    await expect(
      POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/audio/transcription'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('should return 400 if the file in the form data is not of type File', async () => {
    const formData = new FormData();
    formData.append('file', '123');
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: formData
    });

    await expect(
      POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/audio/transcription'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('should return 400 if the file is too big', async () => {
    // @ts-expect-error - intentionally overriding a constant for testing
    vi.spyOn(constants, 'MAX_AUDIO_FILE_SIZE', 'get').mockReturnValueOnce(1);

    const fileContent = new Blob(['dummy content'], { type: 'audio/mp4' });
    const testFile = new File([fileContent], 'test.txt', { type: 'audio/mp4' });
    const request = requestWithFormData(testFile);

    await expect(
      POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/audio/transcription'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
    // Reset the mock after this test
    vi.resetModules();
  });

  it('should return a 500 if there is an error transcribing the file', async () => {
    mockOpenAI.setError('transcription');

    const fileContent = new Blob(['dummy content'], { type: 'audio/mp4' });
    const testFile = new File([fileContent], 'test.txt', { type: 'audio/mp4' });
    const request = requestWithFormData(testFile);

    await expect(
      POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/audio/transcription'
      >)
    ).rejects.toMatchObject({
      status: 500
    });
  });

  it('should return transcribed text', async () => {
    const fileContent = new Blob(['dummy content'], { type: 'audio/mp4' });
    const testFile = new File([fileContent], 'test.txt', { type: 'audio/mp4' });
    const request = requestWithFormData(testFile);

    const res = await POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
      RouteParams,
      '/api/audio/transcription'
    >);
    const data = await res.json();
    expect(data).toEqual({ text: 'Fake transcription' });
  });
});
