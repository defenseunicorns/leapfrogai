import { server } from '../../../vitest-setup';
import { delay, http, HttpResponse } from 'msw';

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
