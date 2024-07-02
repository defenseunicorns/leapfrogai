import { http, HttpResponse } from 'msw';
import type { APIKeyRow } from '$lib/types/apiKeys';
import { server } from '../../../vitest-setup';

export const mockGetKeys = (keys: APIKeyRow[]) => {
  server.use(http.get('/api/api-keys', () => HttpResponse.json(keys)));
};

export const mockDeleteApiKey = () => {
  server.use(http.delete('/api/api-keys/delete', () => new HttpResponse(null, { status: 204 })));
};
