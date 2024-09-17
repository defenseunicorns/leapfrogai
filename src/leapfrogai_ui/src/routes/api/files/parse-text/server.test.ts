import { POST } from './+server';
import { getLocalsMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../../.svelte-kit/types/src/routes/api/files/[file_id]/$types';
import { mockConvertFileErrorNoId, mockConvertFileNoId } from '$lib/mocks/file-mocks';
import type { LFFile } from '$lib/types/files';
import { requestWithFormData } from '$helpers/apiHelpers';
import * as mupdf from 'mupdf';

vi.mock('mupdf', () => ({
  Document: {
    openDocument: vi.fn()
  }
}));

describe('/api/files/parse-text', () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    await expect(
      POST({ request, params: {}, locals: getLocalsMock({ nullSession: true }) } as RequestEvent<
        RouteParams,
        '/api/files/parse-text'
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
        '/api/files/parse-text'
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
        '/api/files/parse-text'
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
        '/api/files/parse-text'
      >)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns 500 if there is an error converting a file to PDF', async () => {
    mockConvertFileErrorNoId();
    const mockFile1: LFFile = new File(['content1'], 'test1.txt', { type: 'text/plain' });
    mockFile1.id = '1';
    const request = requestWithFormData(mockFile1);

    await expect(
      POST({ request, fetch: global.fetch, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/parse-text'
      >)
    ).rejects.toMatchObject({
      status: 500,
      body: { message: 'Error converting file', id: '1' }
    });
  });

  it("returns 500 if there is an error parsing a PDF's text", async () => {
    mupdf.Document.openDocument.mockImplementationOnce(() => {
      throw new Error('Mocked error');
    });

    mockConvertFileNoId('this is ignored');
    const mockFile1: LFFile = new File(['content1'], 'test1.txt', { type: 'text/plain' });
    mockFile1.id = '1';
    const request = requestWithFormData(mockFile1);

    await expect(
      POST({ request, fetch: global.fetch, params: {}, locals: getLocalsMock() } as RequestEvent<
        RouteParams,
        '/api/files/parse-text'
      >)
    ).rejects.toMatchObject({
      status: 500,
      body: { message: 'Mocked error' }
    });
  });

  it('parses text for a PDF file', async () => {
    mupdf.Document.openDocument.mockReturnValue({
      countPages: vi.fn().mockReturnValue(1),
      loadPage: vi.fn().mockReturnValue({
        toStructuredText: vi.fn().mockReturnValue({
          asJSON: vi.fn().mockReturnValue(
            JSON.stringify({
              blocks: [{ lines: [{ text: 'Mocked PDF content' }] }]
            })
          )
        })
      })
    });

    mockConvertFileNoId('this is ignored');
    const mockFile1: LFFile = new File(['this is ignored'], 'test1.txt', { type: 'text/plain' });
    mockFile1.id = '1';

    const request = requestWithFormData(mockFile1);
    const res = await POST({
      request,
      fetch: global.fetch,
      params: {},
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/files/parse-text'>);
    expect(res.status).toEqual(200);
    const resJson = await res.json();

    expect(resJson.text).toEqual('Mocked PDF content');
  });
});
