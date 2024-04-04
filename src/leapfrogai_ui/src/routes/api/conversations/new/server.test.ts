import { faker } from '@faker-js/faker';
import { POST } from './+server';
import { MAX_LABEL_SIZE } from '$lib/constants';
import { getFakeConversation } from '../../../../testUtils/fakeData';
import { sessionMock, sessionNullMock, supabaseInsertMock } from '$lib/mocks/supabase-mocks';

const conversation = getFakeConversation();
const validLabel = faker.string.alpha({ length: MAX_LABEL_SIZE - 1 });
const invalidLongLabel = faker.string.alpha({ length: MAX_LABEL_SIZE + 1 });

describe('/api/conversations/new', () => {
	it('returns a 200 when successful', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST',
			body: JSON.stringify({ label: conversation.label })
		});
		const res = await POST({
			request,
			locals: { getSession: sessionMock, supabase: supabaseInsertMock([conversation]) }
		});

		const resData = await res.json();
		expect(res.status).toEqual(200);
		expect(resData).toEqual(conversation);
	});

	it('returns a 401 when there is no session', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST',
			body: JSON.stringify({ label: validLabel })
		});

		await expect(
			POST({
				request,
				locals: { supabase: supabaseInsertMock([conversation]), getSession: sessionNullMock }
			})
		).rejects.toMatchObject({
			status: 401
		});
	});

	it('returns a 401 when there is no session', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST',
			body: JSON.stringify({ label: validLabel })
		});

		await expect(
			POST({
				request,
				locals: { supabase: supabaseInsertMock([conversation]), getSession: sessionNullMock }
			})
		).rejects.toMatchObject({
			status: 401
		});
	});

	it('returns a 400 when label is too long', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST',
			body: JSON.stringify({ label: invalidLongLabel })
		});

		await expect(
			POST({
				request,
				locals: { supabase: supabaseInsertMock([conversation]), getSession: sessionMock }
			})
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 400 when label is missing', async () => {
		const request = new Request('http://localhost:5173/api/conversations/new', {
			method: 'POST'
		});

		await expect(
			POST({
				request,
				locals: { supabase: supabaseInsertMock([conversation]), getSession: sessionMock }
			})
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
			POST({
				request,
				locals: { supabase: supabaseInsertMock([conversation]), getSession: sessionMock }
			})
		).rejects.toMatchObject({
			status: 400
		});
	});
});
