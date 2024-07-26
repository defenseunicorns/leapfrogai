import { expect, test } from './fixtures';

// TODO - these will not work until we refactor them to flowbite in next PR
test.skip('/api/chat returns a 400 when messages are incorrectly formatted', async ({ request }) => {
  const messages = {
    messages: [{ role: 'user', content: 'test', break: 'me' }]
  };
  const res = await request.post('/api/chat', { data: messages });
  expect(res.status()).toEqual(400);
});

test.skip('/api/threads/delete returns a 400 if the id is not a string', async ({ request }) => {
  const res = await request.delete('/api/threads/delete', {
    data: { id: 123 }
  });
  expect(res.status()).toEqual(400);
});
