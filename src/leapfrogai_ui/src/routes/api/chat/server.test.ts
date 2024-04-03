import { afterAll } from 'vitest';
import { POST } from './+server';

describe('/api/chat', () => {
	beforeAll(() => {
		vi.mock('openai');
	});
	afterAll(() => {
		vi.restoreAllMocks();
	});

	it('returns a 400 when messages are incorrectly formatted', async () => {
		const request = new Request('http://localhost:5173/api/chat', {
			method: 'POST',
			body: JSON.stringify({ messages: [{ break: 'me' }] })
		});

		await expect(POST({ request })).rejects.toMatchObject({ status: 400 });
	});
	it('returns a 400 when messages are missing from the request', async () => {
		const request = new Request('http://localhost:5173/api/chat', {
			method: 'POST'
		});

		await expect(POST({ request })).rejects.toMatchObject({ status: 400 });
	});
	it('returns a 400 when extra body parameters are passed', async () => {
		const validMessage: AIMessage = { content: 'test', role: 'user' };
		const request = new Request('http://localhost:5173/api/chat', {
			method: 'POST',
			body: JSON.stringify({ messages: [validMessage], wrong: 'key' })
		});

		await expect(POST({ request })).rejects.toMatchObject({ status: 400 });
	});
});
