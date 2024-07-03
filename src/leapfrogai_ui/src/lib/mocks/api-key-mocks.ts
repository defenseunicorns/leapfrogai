import { delay, http, HttpResponse } from 'msw';
import { type APIKeyRow, type NewApiKeyInput, PERMISSIONS } from '$lib/types/apiKeys';
import { server } from '../../../vitest-setup';
import { faker } from '@faker-js/faker';

export const mockGetKeys = (keys: APIKeyRow[]) => {
  server.use(
    http.get(`${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/list-api-keys`, () =>
      HttpResponse.json(keys)
    )
  );
};

type MockDeleteApiKeyOptions = {
  withDelay?: boolean;
};
export const mockDeleteApiKey = (options: MockDeleteApiKeyOptions = {}) => {
  server.use(
    http.delete('/api/api-keys/delete', async () => {
      const { withDelay } = options;
      if (withDelay) {
        await delay(200);
      }
      return new HttpResponse(null, { status: 204 });
    })
  );
};

export const mockCreateApiKeyFormAction = (key: APIKeyRow) => {
  server.use(
    http.post('/', () =>
      HttpResponse.json({
        type: 'success',
        status: 200,
        data: `[{"form":1,"key":8},{"id":2,"valid":3,"posted":3,"errors":4,"data":5},"61uqcw",true,{},{"name":6,"expires_at":7},"${key.name}",${key.created_at},{"id":9,"name":10,"api_key":11,"created_at":12,"expires_at":12,"permissions":13},"${key.id}","${key.name}","${key.api_key}",${key.expires_at},"${key.permissions}"]`
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

export const mockRevokeApiKey = () => {
  server.use(
    http.delete(
      `${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/revoke-api-key`,
      () => new HttpResponse(null, { status: 204 })
    )
  );
};

export const mockRevokeApiKeyError = () => {
  server.use(
    http.delete(
      `${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/revoke-api-key`,
      () => new HttpResponse(null, { status: 500 })
    )
  );
};
