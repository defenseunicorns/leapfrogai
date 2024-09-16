import { getAccessToken } from '../fixtures';

export const deleteAllTestAPIKeys = async () => {
  const token = await getAccessToken();
  const res = await fetch(`${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/api-keys`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  const keys = await res.json();
  const promises: Promise<Response>[] = [];
  for (const key of keys) {
    if (key.name.includes('test')) {
      promises.push(
        fetch(`${process.env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/api-keys/${key.id}`, {
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
