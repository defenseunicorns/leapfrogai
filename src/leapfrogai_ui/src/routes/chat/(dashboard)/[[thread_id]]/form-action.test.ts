import { getLocalsMock } from '$lib/mocks/misc';
import type { ActionFailure, RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';
import { actions } from './+page.server';
import { mockConvertFileErrorNoId, mockConvertFileNoId } from '$lib/mocks/file-mocks';
import * as superforms from 'sveltekit-superforms';
import { afterAll } from 'vitest';

vi.mock('mupdf', () => ({
  Document: {
    openDocument: vi.fn().mockReturnValue({
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
    })
  }
}));

describe('chat page form action', () => {
  afterAll(() => {
    vi.restoreAllMocks();
  });
  it('returns a 401 if the request is unauthenticated', async () => {
    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST'
    });
    const res = await actions.default({
      request,
      locals: getLocalsMock({ nullSession: true })
    } as RequestEvent<RouteParams, '/chat/(dashboard)/[[thread_id]]'>);

    expect(res?.status).toEqual(401);
  });

  it('returns a 400 if the request data is invalid', async () => {
    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST'
    });

    const res = await actions.default({ request, locals: getLocalsMock() } as RequestEvent<
      RouteParams,
      '/chat/(dashboard)/[[thread_id]]'
    >);
    expect(res?.status).toEqual(400);
  });

  it('returns a 400 if after validation there are no files', async () => {
    vi.spyOn(superforms, 'superValidate').mockResolvedValue({
      valid: true,
      data: {
        files: []
      },
      id: '',
      posted: false,
      errors: {}
    });

    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    const res = (await actions.default({
      request,
      fetch: global.fetch,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/chat/(dashboard)/[[thread_id]]'>)) as ActionFailure;

    expect(res?.status).toEqual(400);
  });

  it('sets a file to error status if there is an error converting it', async () => {
    mockConvertFileErrorNoId();

    const mockFile1 = new File(['content1'], 'test1.txt', { type: 'text/plain' });

    vi.spyOn(superforms, 'superValidate').mockResolvedValue({
      valid: true,
      data: {
        files: [mockFile1]
      },
      id: '',
      posted: false,
      errors: {}
    });

    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    const res = (await actions.default({
      request,
      fetch: global.fetch,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/chat/(dashboard)/[[thread_id]]'>)) as ActionFailure;

    expect(res.extractedFilesText[0].status).toEqual('error');
  });

  it('sets a file to error status if there is an error converting it', async () => {
    mockConvertFileErrorNoId();

    const mockFile1 = new File(['content1'], 'test1.txt', { type: 'text/plain' });

    vi.spyOn(superforms, 'superValidate').mockResolvedValue({
      valid: true,
      data: {
        files: [mockFile1]
      },
      id: '',
      posted: false,
      errors: {}
    });

    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    const res = (await actions.default({
      request,
      fetch: global.fetch,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/chat/(dashboard)/[[thread_id]]'>)) as ActionFailure;

    expect(res.extractedFilesText[0].status).toEqual('error');
  });

  it('returns files with their text content', async () => {
    mockConvertFileNoId('this is ignored');

    const mockFile1 = new File(['this is ignored'], 'test1.txt', { type: 'text/plain' });

    vi.spyOn(superforms, 'superValidate').mockResolvedValue({
      valid: true,
      data: {
        files: [mockFile1]
      },
      id: '',
      posted: false,
      errors: {}
    });

    const request = new Request('https://thisurldoesntmatter', {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    const res = (await actions.default({
      request,
      fetch: global.fetch,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/chat/(dashboard)/[[thread_id]]'>)) as ActionFailure;

    expect(res.extractedFilesText[0].status).toEqual('complete');
    expect(res.extractedFilesText[0].text).toEqual('Mocked PDF content');
  });
});
