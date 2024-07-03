import { env } from '$env/dynamic/private';
import { getToken } from '../fixtures';

// TODO - get this teardown to work
// TODO - refactor page to move modals to own components?
// TODO - record demo and submit PR
export const deleteAllTestAPIKeys = async () => {
  const token = getToken();
  const res = await fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/list-api-keys`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  const keys = await res.json();
  const promises: Promise<Response>[] = [];
  for (const key of keys) {
    if (key.name.includes('test')) {
      promises.push(
        fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/revoke-api-key/${id}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      );
    }
  }
  await Promise.allSettled(promises);
};
