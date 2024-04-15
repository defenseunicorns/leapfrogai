import { faker } from '@faker-js/faker';
import {
	sessionMock,
	sessionNullMock,
	supabaseUpdateErrorMock,
	supabaseUpdateMock
} from '$lib/mocks/supabase-mocks';
import { MAX_LABEL_SIZE } from '$lib/constants';
import { PUT } from './+server';

const validLabel = faker.string.alpha({ length: MAX_LABEL_SIZE - 1 });
const invalidLongLabel = faker.string.alpha({ length: MAX_LABEL_SIZE + 1 });

describe('/api/conversations/update', () => {
	it('returns a 204 when successful', async () => {
		const request = new Request('http://localhost:5173/api/conversations/update/label', {
			method: 'POST',
			body: JSON.stringify({ id: faker.string.uuid(), label: validLabel })
		});
		const res = await PUT({
			request,
			locals: { getSession: sessionMock, supabase: supabaseUpdateMock() }
		});

		expect(res.status).toEqual(204);
	});

	it('returns a 401 when there is no session', async () => {
		const request = new Request('http://localhost:5173/api/conversations/update/label', {
			method: 'PUT',
			body: JSON.stringify({ id: faker.string.uuid(), label: validLabel })
		});

		await expect(
			PUT({
				request,
				locals: { supabase: {}, getSession: sessionNullMock }
			})
		).rejects.toMatchObject({
			status: 401
		});
	});

	it('returns a 400 when id is not a uuid', async () => {
		const request = new Request('http://localhost:5173/api/conversations/update/label', {
			method: 'PUT',
			body: JSON.stringify({ id: '123', label: validLabel })
		});

		await expect(
			PUT({ request, locals: { supabase: {}, getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 400 when id is missing', async () => {
		const request = new Request('http://localhost:5173/api/conversations/update/label', {
			method: 'PUT',
			body: JSON.stringify({ label: validLabel })
		});

		await expect(
			PUT({ request, locals: { supabase: {}, getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 400
		});
	});

	it('returns a 400 when the label is too long', async () => {
		const request = new Request('http://localhost:5173/api/conversations/update/label', {
			method: 'PUT',
			body: JSON.stringify({ id: faker.string.uuid(), label: invalidLongLabel })
		});

		await expect(
			PUT({ request, locals: { supabase: {}, getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 400 when the label is missing', async () => {
		const request = new Request('http://localhost:5173/api/conversations/update/label', {
			method: 'PUT',
			body: JSON.stringify({ id: faker.string.uuid() })
		});

		await expect(
			PUT({ request, locals: { supabase: {}, getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 400 when extra body parameters are passed', async () => {
		const request = new Request('http://localhost:5173/api/conversations/update/label', {
			method: 'PUT',
			body: JSON.stringify({ id: faker.string.uuid(), label: validLabel, break: 'me' })
		});

		await expect(
			PUT({ request, locals: { supabase: {}, getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 400
		});
	});
	it('returns a 500 when there is a supabase error', async () => {
		const request = new Request('http://localhost:5173/api/conversations/update/label', {
			method: 'PUT',
			body: JSON.stringify({ id: faker.string.uuid(), label: validLabel })
		});

		await expect(
			PUT({ request, locals: { supabase: supabaseUpdateErrorMock(), getSession: sessionMock } })
		).rejects.toMatchObject({
			status: 500
		});
	});
});
