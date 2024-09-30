import { server } from '../../../vitest-setup';
import { delay, http, HttpResponse } from 'msw';
import type { FileObject } from 'openai/resources/files';
import type { LFAssistant } from '$lib/types/assistants';

export const mockDeleteFile = () => {
  server.use(http.delete('/api/files/delete', () => new HttpResponse(null, { status: 204 })));
};

export const mockDeleteFileWithDelay = () => {
  server.use(
    http.delete('/api/files/delete', async () => {
      await delay(500);
      return new HttpResponse(null, { status: 204 });
    })
  );
};

export const mockGetFiles = (files: FileObject[]) => {
  server.use(http.get('/api/files', () => HttpResponse.json(files)));
};

export const mockGetFile = (id: string, fileContent: string, contentType = 'application/pdf') => {
  server.use(
    http.get(
      `/api/files/${id}`,
      () =>
        new Response(new Blob([fileContent], { type: contentType }), {
          headers: {
            'Content-Type': contentType
          }
        })
    )
  );
};

export const mockGetFileError = (id: string) => {
  server.use(http.get(`/api/files/${id}`, async () => new HttpResponse(null, { status: 500 })));
};

export const mockConvertFile = (id: string, fileContent: string) => {
  server.use(
    http.get(
      `/api/files/convert/${id}`,
      () =>
        new Response(new Blob([fileContent], { type: 'application/pdf' }), {
          headers: {
            'Content-Type': 'application/pdf'
          }
        })
    )
  );
};

export const mockConvertFileNoId = (fileContent: string) => {
  server.use(
    http.post(
      `/api/files/convert`,
      () =>
        new Response(new Blob([fileContent], { type: 'application/pdf' }), {
          headers: {
            'Content-Type': 'application/pdf'
          }
        })
    )
  );
};

export const mockConvertFileError = (id: string) => {
  server.use(
    http.get(`/api/files/convert/${id}`, async () => new HttpResponse(null, { status: 500 }))
  );
};

export const mockConvertFileErrorNoId = () => {
  server.use(http.post(`/api/files/convert`, async () => new HttpResponse(null, { status: 500 })));
};

export const mockDeleteCheck = (assistantsToReturn: LFAssistant[]) => {
  server.use(
    http.post('/api/files/delete/check', async () => {
      await delay(100);
      return HttpResponse.json(assistantsToReturn);
    })
  );
};

export const mockDownloadError = (id: string) => {
  server.use(http.get(`api/files/${id}`, () => new HttpResponse(null, { status: 500 })));
};
