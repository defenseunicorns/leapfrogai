import { POST } from './+server';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';
import { afterAll } from 'vitest';
import { requestWithFormData } from '$helpers/apiHelpers';

// Allows swapping out the mock per test
const mocks = vi.hoisted(() => {
  return {
    convert: vi.fn()
  };
});

vi.mock('libreoffice-convert', () => ({
  default: {
    convert: mocks.convert
  }
}));

describe('/api/files/convert', () => {
  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    await expect(
      POST({ request, params: {}, locals: getLocalsMock({ nullSession: true }) } as RequestEvent<
        RouteParams,
        '/api/files/convert'
      >)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('should return 400 if the form data is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    await expect(
      POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('should return 400 if the file is missing from the form data', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: new FormData()
    });

    await expect(
      POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert'
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
        '/api/files/convert'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 500 if there is an error converting the file', async () => {
    mocks.convert.mockImplementation((buffer, ext, options, callback) => {
      callback(new Error('Mocked convertAsync error'));
    });

    const fileContent = new Blob(['dummy content'], { type: 'text/plain' });
    const testFile = new File([fileContent], 'test.txt', { type: 'text/plain' });
    const request = requestWithFormData(testFile);

    await expect(
      POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert'
      >)
    ).rejects.toMatchObject({
      status: 500
    });
  });

  it('converts the file', async () => {
    mocks.convert.mockImplementation((buffer, ext, options, callback) => {
      const pdfBuffer = Buffer.from('testPdf');
      callback(null, pdfBuffer);
    });

    const fileContent = new Uint8Array([
      100, 117, 109, 109, 121, 32, 99, 111, 110, 116, 101, 110, 116
    ]); // dummy content

    const testFile = new File([fileContent], 'test.txt', { type: 'text/plain' });
    testFile.arrayBuffer = async () => fileContent.buffer;

    const request = requestWithFormData(testFile);

    const res = await POST({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
      RouteParams,
      '/api/files/convert'
    >);
    expect(res.status).toEqual(200);
    expect(res.headers.get('Content-Type')).toBe('application/pdf');
    const buffer = await res.arrayBuffer();
    const pdfText = new TextDecoder().decode(buffer);
    expect(pdfText).toContain('testPdf');
  });
});
