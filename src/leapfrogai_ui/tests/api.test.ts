import { test, expect } from '@playwright/test';

test('/api/chat returns a 400 when messages are incorrectly formatted', async ({ request }) => {
	const messages = {
		messages: [{ role: 'user', content: 'test', break: 'me' }]
	};
	const res = await request.post('/api/chat', { data: messages });
	expect(res.status()).toEqual(400);
});

