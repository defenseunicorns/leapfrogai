import { POST } from './+server';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';
import { afterAll } from 'vitest';
import { fileSchema } from '$schemas/files';

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

    // When creating the file below, it fails the yup validation for not being an instance of File even though it is
    // we are mocking the validation here to get past that issue
    vi.spyOn(fileSchema, 'validate').mockResolvedValueOnce({});

    const formData = new FormData();
    const fileContent = new Blob(['dummy content'], { type: 'text/plain' });
    const testFile = new File([fileContent], 'test.txt', { type: 'text/plain' });
    formData.append('file', testFile);

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
      status: 500
    });
  });

  it('converts the file', async () => {
    mocks.convert.mockImplementation((buffer, ext, options, callback) => {
      const pdfBuffer = Buffer.from('testPdf');
      callback(null, pdfBuffer);
    });

    // When creating the file below, it fails the yup validation for not being an instance of File even though it is
    // we are mocking the validation here to get past that issue
    vi.spyOn(fileSchema, 'validate').mockResolvedValueOnce({});

    const formData = new FormData();
    const fileContent = new Blob(['dummy content'], { type: 'text/plain' });
    const testFile = new File([fileContent], 'test.txt', { type: 'text/plain' });
    formData.append('file', testFile);

    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: formData
    });

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
