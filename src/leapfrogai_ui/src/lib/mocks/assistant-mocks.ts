import { server } from '../../../vitest-setup';
import { bypass, http, HttpResponse } from 'msw';

export const mockNewAssistantError = () => {
  server.use(http.post('/api/assistants/new', () => new HttpResponse(null, { status: 500 })));
};

export const allowAssistantPost = () => {
  server.use(
    http.post('/', async ({ request }) => {
      // Perform the intercepted "GET /user" request as-is
      // by passing its "request" reference to the "bypass" function.
      await fetch(bypass(request));
    })
  );
};
