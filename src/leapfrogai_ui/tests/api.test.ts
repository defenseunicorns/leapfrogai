import { test, expect } from '@playwright/test';

test.skip('/api/chat returns a 400 when messages are incorrectly formatted', async ({ request }) => {
	const messages = {
		messages: [{ role: 'user', content: 'test', break: 'me' }]
	};
	const res = await request.post('/api/chat', { data: messages });
	expect(res.status()).toEqual(400);
});

test.skip('/api/chat returns an AI response', async ({ request }) => {
	const messages = {
		messages: [{ role: 'user', content: 'test' }]
	};
	const res = await request.post('/api/chat', { data: messages });
	const message = await res.json();
	console.log(message);
	expect(message.length).toBeGreaterThan(0);
});
