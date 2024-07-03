import { http, HttpResponse } from 'msw';
import { type APIKeyRow, type NewApiKeyInput, PERMISSIONS } from '$lib/types/apiKeys';
import { server } from '../../../vitest-setup';
import { faker } from '@faker-js/faker';
import type { ActionResult } from '@sveltejs/kit';

export const mockGetKeys = (keys: APIKeyRow[]) => {
  server.use(
    http.get(`${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/list-api-keys`, () =>
      HttpResponse.json(keys)
    )
  );
};

export const mockDeleteApiKey = () => {
  server.use(
    http.delete(
      `${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/revoke-api-key`,
      () => new HttpResponse(null, { status: 204 })
    )
  );
};

export const mockCreateApiKeyFormAction = (name: string, api_key: string, expires_at: number) => {
  server.use(
    http.post('/', () =>
      HttpResponse.json({
        type: 'success',
        status: 200,
        data: `[{\"form\":1,\"key\":8},{\"id\":2,\"valid\":3,\"posted\":3,\"errors\":4,\"data\":5},\"61uqcw\",true,{},{\"name\":6,\"expires_at\":7},\"${name}\",${expires_at},\"${api_key}\"]`
      })
    )
  );
};

export const mockCreateApiKey = (api_key = `lfai_${faker.string.uuid()}`) => {
  server.use(
    http.post(
      `${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/create-api-key`,
      async ({ request }) => {
        const reqJson = (await request.json()) as NewApiKeyInput;
        const key: APIKeyRow = {
          id: faker.string.uuid(),
          name: reqJson.name,
          api_key,
          created_at: new Date().getTime(),
          expires_at: reqJson.expires_at,
          permissions: PERMISSIONS.ALL
        };
        return HttpResponse.json(key);
      }
    )
  );
};

export const mockCreateApiKeyError = () => {
  server.use(
    http.post(
      `${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/create-api-key`,
      async () => new HttpResponse(null, { status: 500 })
    )
  );
};
