import { server } from '../../../vitest-setup';
import { delay, http, HttpResponse } from 'msw';
import type { FileObject } from 'openai/resources/files';

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
