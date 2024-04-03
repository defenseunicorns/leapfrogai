import { test, expect } from '@playwright/test';

test('/api/chat returns a 400 when messages are incorrectly formatted', async ({ request }) => {
	const messages = {
		messages: [{ role: 'user', content: 'test', break: 'me' }]
	};
	const res = await request.post('/api/chat', { data: messages });
	expect(res.status()).toEqual(400);
});

test('/api/conversations/delete returns a 400 if the id is not a uuid', async ({request}) => {
	const res = await request.delete('/api/conversations/delete', {data: {conversationId: "123"}});
	expect(res.status()).toEqual(400);
});