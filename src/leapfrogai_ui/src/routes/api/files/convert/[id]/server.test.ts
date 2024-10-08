import { GET } from './+server';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';
import { mockOpenAI } from '../../../../../../vitest-setup';
import { faker } from '@faker-js/faker';
import { getFakeFiles } from '$testUtils/fakeData';
import { afterAll } from 'vitest';

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

describe('/api/files/convert/[id]', () => {
  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    await expect(
      GET({ request, params: {}, locals: getLocalsMock({ nullSession: true }) } as RequestEvent<
        RouteParams,
        '/api/files/convert/[id]'
      >)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('should return 400 if file id is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    await expect(
      GET({ request, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert/[id]'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('should return 400 if file id is not a string', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    await expect(
      // @ts-expect-error - we want to test this error
      GET({ request, params: { id: 123 }, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert/[id]'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 404 if the file metadata is not found', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    await expect(
      GET({ request, params: { id: 'fakeId123' }, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert/[id]'
      >)
    ).rejects.toMatchObject({
      status: 404
    });
  });
  it('returns a 500 if there is an error getting the file content', async () => {
    const files = getFakeFiles();
    mockOpenAI.setFiles(files);
    mockOpenAI.setError('fileContent');

    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    await expect(
      GET({ request, params: { id: files[0].id }, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert/[id]'
      >)
    ).rejects.toMatchObject({
      status: 500
    });
  });
  it('returns a 404 if the file content is undefined or null', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    await expect(
      GET({ request, params: { id: faker.string.uuid() }, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert/[id]'
      >)
    ).rejects.toMatchObject({
      status: 404
    });
  });

  it('returns a 500 if there is an error converting the file', async () => {
    mocks.convert.mockImplementation((buffer, ext, options, callback) => {
      callback(new Error('Mocked convertAsync error'));
    });

    const files = getFakeFiles();
    mockOpenAI.setFiles(files);

    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    await expect(
      GET({ request, params: { id: files[0].id }, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/convert/[id]'
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

    const files = getFakeFiles();
    mockOpenAI.setFiles(files);

    const request = new Request('http://thisurlhasnoeffect', {
      method: 'GET'
    });

    const res = await GET({
      request,
      params: { id: files[0].id },
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/files/convert/[id]'>);
    expect(res.status).toEqual(200);
    expect(res.headers.get('Content-Type')).toBe('application/pdf');
    const buffer = await res.arrayBuffer();
    const pdfText = new TextDecoder().decode(buffer);
    expect(pdfText).toContain('testPdf');
  });
});
