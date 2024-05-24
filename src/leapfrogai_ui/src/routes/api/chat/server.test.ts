import { afterAll } from 'vitest';
import type { ChatCompletionMessageParam } from 'ai/prompts';
import { POST } from './+server';
import { sessionMock, sessionNullMock } from '$lib/mocks/supabase-mocks';

describe('/api/chat', () => {
  beforeAll(() => {
    vi.mock('openai');
  });
  afterAll(() => {
    vi.restoreAllMocks();
  });

  // NOTE - message streaming success is tested via E2E test

  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ messages: [] })
    });

    await expect(
      POST({
        request,
        locals: { safeGetSession: sessionNullMock }
      })
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when messages are incorrectly formatted', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ messages: [{ break: 'me' }] })
    });

    await expect(POST({ request, locals: { safeGetSession: sessionMock } })).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when messages are missing from the request', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    await expect(POST({ request, locals: { safeGetSession: sessionMock } })).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when extra body parameters are passed', async () => {
    const validMessage: ChatCompletionMessageParam = { content: 'test', role: 'user' };
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ messages: [validMessage], wrong: 'key' })
    });

    await expect(POST({ request, locals: { safeGetSession: sessionMock } })).rejects.toMatchObject({
      status: 400
    });
  });
});
