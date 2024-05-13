import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { afterAll, beforeAll, type MockInstance, vi } from 'vitest';
import * as navigation from '$app/navigation';
import NewAssistantPage from './+page.svelte';
import { ASSISTANTS_DESCRIPTION_MAX_LENGTH, ASSISTANTS_NAME_MAX_LENGTH } from '$lib/constants';
import { actions, load } from './+page.server';
import {
  sessionMock,
  sessionNullMock,
  supabaseInsertErrorMock,
  supabaseInsertMock
} from '$lib/mocks/supabase-mocks';
import { getFakeAssistant } from '../../../../../../testUtils/fakeData';
import type { PageServerLoad } from './$types';

describe('New Assistant page', () => {
  let goToSpy: MockInstance;

  let data: PageServerLoad;

  beforeAll(async () => {
    data = await load({ locals: { getSession: sessionMock } });
    goToSpy = vi.spyOn(navigation, 'goto');
  });

  afterEach(() => {
    vi.clearAllMocks();
  });
  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('has a modal that navigates back to the management page', async () => {
    render(NewAssistantPage, { data });

    const cancelBtn = screen.getAllByRole('button', { name: /cancel/i })[0];
    await userEvent.click(cancelBtn);

    await userEvent.click(screen.getByText('Leave this page'));

    expect(goToSpy).toHaveBeenCalledWith('/chat/assistants-management');
  });
  it('has a modal that stays on page when canceled', async () => {
    render(NewAssistantPage, { data });

    const cancelBtn = screen.getAllByRole('button', { name: /cancel/i })[0];
    await userEvent.click(cancelBtn);

    await userEvent.click(screen.getByText('Stay on page'));

    expect(goToSpy).toHaveBeenCalledTimes(0);
  });

  it('limits the name input length', async () => {
    render(NewAssistantPage, { data });
    const nameField = screen.getByRole('textbox', { name: /name/i });
    await userEvent.type(nameField, 'a'.repeat(ASSISTANTS_NAME_MAX_LENGTH + 1));
    expect(nameField).toHaveValue('a'.repeat(ASSISTANTS_NAME_MAX_LENGTH));
  });

  it('limits the description input length', async () => {
    render(NewAssistantPage, { data });
    const descriptionField = screen.getByRole('textbox', { name: /description/i });
    await userEvent.type(descriptionField, 'a'.repeat(ASSISTANTS_DESCRIPTION_MAX_LENGTH + 1));
    expect(descriptionField).toHaveValue('a'.repeat(ASSISTANTS_DESCRIPTION_MAX_LENGTH));
  });
  /* Note - instructions length limit is too long, test times out.
     Attempts to mock the constant required specifying each variable from the constants file in the mock
     (vi.importActual) did not work
     The extra maintenance overhead was deemed not worth testing this field
  */

  describe('the new assistant server side form action', () => {
    it('redirects on success', async () => {
      const assistant = getFakeAssistant();
      const formData = new FormData();
      formData.append('name', assistant.name!);
      formData.append('description', assistant.description!);
      formData.append('instructions', assistant.instructions!);
      formData.append('data_sources', '');
      formData.append('pictogram', 'User');

      const request = new Request('http://localhost:5173/chat/assistants-management/new', {
        method: 'POST',
        body: formData
      });

      // Redirect from sveltekit throws
      try {
        await actions.default({
          request,
          locals: { supabase: supabaseInsertMock([assistant]), getSession: sessionMock }
        });
      } catch (redirect) {
        expect(redirect?.status).toEqual(303);
        expect(redirect?.location).toBe('/chat/assistants-management');
      }
    });

    it('returns a 401 if the request is unauthenticated', async () => {
      const request = new Request('http://localhost:5173/chat/assistants-management/new', {
        method: 'POST'
      });
      const res = await actions.default({
        request,
        locals: { supabase: supabaseInsertMock, getSession: sessionNullMock }
      });

      expect(res.status).toEqual(401);
    });
  });
  it('returns a 400 if the form data is invalid', async () => {
    const formData = new FormData();
    formData.append('name', 'My Assistant');

    const request = new Request('http://localhost:5173/chat/assistants-management/new', {
      method: 'POST',
      body: formData
    });
    const res = await actions.default({
      request,
      locals: { supabase: supabaseInsertMock({}), getSession: sessionMock }
    });

    expect(res.status).toEqual(400);
  });

  it('returns a 500 when there is a supabase error saving the assistant', async () => {
    const formData = new FormData();
    formData.append('name', 'My Assistant');
    formData.append('description', 'This is an assistant');
    formData.append('instructions', 'Be a helpful assistant');
    formData.append('data_sources', '');
    formData.append('pictogram', 'User');

    const request = new Request('http://localhost:5173/chat/assistants-management/new', {
      method: 'POST',
      body: formData
    });
    const res = await actions.default({
      request,
      locals: { supabase: supabaseInsertErrorMock(), getSession: sessionMock }
    });

    expect(res.status).toEqual(500);
  });
});
