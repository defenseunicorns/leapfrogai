import { faker } from '@faker-js/faker';
import { DELETE } from './+server';
import {
	sessionMock,
	sessionNullMock,
	supabaseDeleteErrorMock,
	supabaseDeleteMock
} from '$lib/mocks/supabase-mocks';

describe('/api/conversations/delete', () => {
	it('returns a 204 when the request completes', async () => {
		const request = new Request('http://localhost:5173/api/conversations/delete', {
			method: 'DELETE',
			body: JSON.stringify({ conversationId: faker.string.uuid() })
		});

		const res = await DELETE({
			request,
			locals: { supabase: supabaseDeleteMock(), getSession: sessionMock }
		});
		expect(res.status).toEqual(204);
	});
	it('returns a 401 when there is no session', async () => {
		const request = new Request('http://localhost:5173/api/conversations/delete', {
			method: 'DELETE',
			body: JSON.stringify({ conversationId: faker.string.uuid() })
		});

		await expect(
			DELETE({
				request,
				locals: { supabase: {}, getSession: sessionNullMock }
			})
		).rejects.toMatchObject({
			status: 401
		});
	});

	it('returns a 400 when conversationId is not a uuid', async () => {
		const request = new Request('http://localhost:5173/api/conversations/delete', {
			method: 'DELETE',
			body: JSON.stringify({ conversationId: '123' })
		});

		await expect(
			DELETE({ request, locals: { supabase: {}, getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 400 when conversationId is missing', async () => {
		const request = new Request('http://localhost:5173/api/conversations/delete', {
			method: 'DELETE'
		});

		await expect(
			DELETE({ request, locals: { supabase: {}, getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 400 when extra body arguments are passed', async () => {
		const request = new Request('http://localhost:5173/api/conversations/delete', {
			method: 'DELETE',
			body: JSON.stringify({ conversationId: faker.string.uuid(), wrong: 'key' })
		});

		await expect(
			DELETE({ request, locals: { supabase: {}, getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 400
		});
	});

	it('returns a 500 when there is a supabase error', async () => {
		const request = new Request('http://localhost:5173/api/conversations/delete', {
			method: 'DELETE',
			body: JSON.stringify({ conversationId: faker.string.uuid() })
		});

		await expect(
			DELETE({ request, locals: { supabase: supabaseDeleteErrorMock(), getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 500
		});
	});
});
