import { faker } from '@faker-js/faker';
import { POST } from './+server';
import { MAX_LABEL_SIZE } from '$lib/constants';

const validLabel = faker.string.alpha({ length: MAX_LABEL_SIZE - 1 });
const invalidLongLabel = faker.string.alpha({ length: MAX_LABEL_SIZE + 1 });

describe('/api/conversations/new', () => {
	// TODO - add functionality other endpoints
	it('redirects when there is no session', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST',
			body: JSON.stringify({ label: validLabel })
		});

		await expect(
			POST({ request, locals: { supabase: {}, getSession: vi.fn(() => Promise.resolve(null)) } })
		).rejects.toMatchObject({
			status: 303,
			location: '/'
		});
	});
	// TODO - success when there is a session
	it('returns a 400 when label is too long', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST',
			body: JSON.stringify({ label: invalidLongLabel })
		});

		await expect(
			POST({ request, locals: { supabase: {}, getSession: vi.fn() } })
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 400 when label is missing', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST'
		});

		await expect(
			POST({ request, locals: { supabase: {}, getSession: vi.fn() } })
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 400 when extra body arguments are passed', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST',
			body: JSON.stringify({ label: validLabel, wrong: 'key' })
		});

		await expect(
			POST({ request, locals: { supabase: {}, getSession: vi.fn() } })
		).rejects.toMatchObject({
			status: 400
		});
	});
});
