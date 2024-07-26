import { expect, test } from './fixtures';

test('/api/chat returns a 400 when messages are incorrectly formatted', async ({ request }) => {
  const messages = {
    messages: [{ role: 'user', content: 'test', break: 'me' }]
  };
  const res = await request.post('/api/chat', { data: messages });
  expect(res.status()).toEqual(400);
});

test('/api/threads/delete returns a 400 if the id is not a string', async ({ request }) => {
  const res = await request.delete('/api/threads/delete', {
    data: { id: 123 }
  });
  expect(res.status()).toEqual(400);
});
