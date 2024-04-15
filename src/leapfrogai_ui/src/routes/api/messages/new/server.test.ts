import {
	sessionMock,
	sessionNullMock,
	supabaseInsertErrorMock,
	supabaseInsertMock
} from '$lib/mocks/supabase-mocks';
import { getFakeMessage } from '../../../../testUtils/fakeData';
import { POST } from './+server';

const message = getFakeMessage({});

const validMessageBody = {
	content: message.content,
	conversation_id: message.conversation_id,
	role: message.role
};

describe('/api/messages/new', () => {
	it('returns a 200 when successful', async () => {
		const request = new Request('http://localhost:5173/api/messages/new', {
			method: 'POST',
			body: JSON.stringify(validMessageBody)
		});

		const res = await POST({
			request,
			locals: { getSession: sessionMock, supabase: supabaseInsertMock([message]) }
		});

		const resData = await res.json();
		expect(res.status).toEqual(200);
		expect(resData).toEqual(message);
	});

	it('returns a 401 when there is no session', async () => {
		const request = new Request('http://localhost:5173/api/messages/new', {
			method: 'POST',
			body: JSON.stringify(validMessageBody)
		});

		await expect(
			POST({
				request,
				locals: { supabase: supabaseInsertMock([message]), getSession: sessionNullMock }
			})
		).rejects.toMatchObject({
			status: 401
		});
	});
	it('returns a 400 when the body is invalid', async () => {
		// Empty body
		let request = new Request('http://localhost:5173/api/messages/new', {
			method: 'POST'
		});

		await expect(
			POST({
				request,
				locals: { supabase: supabaseInsertMock([message]), getSession: sessionMock }
			})
		).rejects.toMatchObject({
			status: 400
		});

		// Invalid param
		request = new Request('http://localhost:5173/api/messages/new', {
			method: 'POST',
			body: JSON.stringify({ ...validMessageBody, id: '123' })
		});

		await expect(
			POST({
				request,
				locals: { supabase: supabaseInsertMock([message]), getSession: sessionMock }
			})
		).rejects.toMatchObject({
			status: 400
		});

		// Extra param
		request = new Request('http://localhost:5173/api/messages/new', {
			method: 'POST',
			body: JSON.stringify({ ...validMessageBody, break: 'me' })
		});

		await expect(
			POST({
				request,
				locals: { supabase: supabaseInsertMock([message]), getSession: sessionMock }
			})
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 500 when there is a supabase error', async () => {
		const request = new Request('http://localhost:5173/api/messages/new', {
			method: 'POST',
			body: JSON.stringify(validMessageBody)
		});

		await expect(
			POST({ request, locals: { supabase: supabaseInsertErrorMock(), getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 500
		});
	});
});
