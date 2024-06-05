import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { afterAll, beforeAll, type MockInstance, vi } from 'vitest';
import * as navigation from '$app/navigation';
import { ASSISTANTS_DESCRIPTION_MAX_LENGTH, ASSISTANTS_NAME_MAX_LENGTH } from '$lib/constants';
import { actions as editActions } from './edit/[assistantId]/+page.server';
import { actions as newActions, load as newLoad } from './new/+page.server';
import {
  sessionMock,
  sessionNullMock,
  storageRemoveMock,
  supabaseInsertSingleMock,
  supabaseStorageMockWrapper
} from '$lib/mocks/supabase-mocks';
import { getFakeAssistant, getFakeAssistantInput } from '$testUtils/fakeData';
import AssistantForm from '$components/AssistantForm.svelte';
import { mockOpenAI } from '../../../../../vitest-setup';

describe('Assistant Form', () => {
  let goToSpy: MockInstance;

  beforeAll(async () => {
    goToSpy = vi.spyOn(navigation, 'goto');
  });

  afterEach(() => {
    vi.clearAllMocks();
  });
  afterAll(() => {
    vi.restoreAllMocks();
  });

  it('has a modal that navigates back to the management page', async () => {
    const data = await newLoad({ locals: { safeGetSession: sessionMock } });
    render(AssistantForm, { data });

    const cancelBtn = screen.getAllByRole('button', { name: /cancel/i })[1];
    await userEvent.click(cancelBtn);

    expect(goToSpy).toHaveBeenCalledWith('/chat/assistants-management');
  });

  it('limits the name input length', async () => {
    const data = await newLoad({ locals: { safeGetSession: sessionMock } });
    render(AssistantForm, { data });
    const nameField = screen.getByRole('textbox', { name: /name/i });
    await userEvent.type(nameField, 'a'.repeat(ASSISTANTS_NAME_MAX_LENGTH + 1));
    expect(nameField).toHaveValue('a'.repeat(ASSISTANTS_NAME_MAX_LENGTH));
  });

  it('limits the description input length', async () => {
    const data = await newLoad({ locals: { safeGetSession: sessionMock } });
    render(AssistantForm, { data });
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
      const assistant = getFakeAssistantInput();

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
        await newActions.default({
          request,
          locals: { supabase: supabaseInsertSingleMock(assistant), safeGetSession: sessionMock }
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
      const res = await newActions.default({
        request,
        locals: { supabase: {}, safeGetSession: sessionNullMock }
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
    const res = await newActions.default({
      request,
      locals: { supabase: {}, safeGetSession: sessionMock }
    });

    expect(res.status).toEqual(400);
  });

  describe('the edit assistant server side form action', () => {
    it('redirects on success', async () => {
      const assistant = getFakeAssistant();

      const formData = new FormData();
      formData.append('id', assistant.id!);
      formData.append('name', assistant.name!);
      formData.append('description', assistant.description!);
      formData.append('instructions', assistant.instructions!);
      formData.append('data_sources', '');
      formData.append('pictogram', 'User');
      // No avatar or avatarFile included to ensure we test the deletion call and mock for the avatar

      const request = new Request(
        `http://localhost:5173/chat/assistants-management/edit/${assistant.id}`,
        {
          method: 'POST',
          body: formData
        }
      );

      // Redirect from sveltekit throws
      try {
        await editActions.default({
          request,
          locals: {
            supabase: supabaseStorageMockWrapper({
              ...storageRemoveMock()
            }),
            safeGetSession: sessionMock
          }
        });
      } catch (redirect) {
        expect(redirect?.status).toEqual(303);
        expect(redirect?.location).toBe('/chat/assistants-management');
      }
    });

    it('returns a 401 if the request is unauthenticated', async () => {
      const request = new Request(`http://localhost:5173/chat/assistants-management/edit/123`, {
        method: 'POST'
      });
      const res = await editActions.default({
        request,
        locals: { supabase: {}, safeGetSession: sessionNullMock }
      });

      expect(res.status).toEqual(401);
    });
    it('returns a 400 if the form data is invalid', async () => {
      const assistant = getFakeAssistant();

      const formData = new FormData();
      formData.append('id', assistant.id!);
      formData.append('name', assistant.name!);

      const request = new Request(
        `http://localhost:5173/chat/assistants-management/edit/${assistant.id}`,
        {
          method: 'POST',
          body: formData
        }
      );

      const res = await editActions.default({
        request,
        locals: { supabase: {}, safeGetSession: sessionMock }
      });

      expect(res.status).toEqual(400);
    });

    it('returns a 500 when there is a openai error saving the assistant', async () => {
      mockOpenAI.setError('updateAssistant');
      const assistant = getFakeAssistant();

      const formData = new FormData();
      formData.append('id', assistant.id!);
      formData.append('name', 'My Assistant');
      formData.append('description', 'This is an assistant');
      formData.append('instructions', 'Be a helpful assistant');
      formData.append('data_sources', '');
      formData.append('avatar', 'fakeUploadUrl');
      formData.append('pictogram', 'User');

      const request = new Request(
        `http://localhost:5173/chat/assistants-management/edit/${assistant.id}`,
        {
          method: 'POST',
          body: formData
        }
      );
      const res = await editActions.default({
        request,
        locals: {
          supabase: {},
          safeGetSession: sessionMock
        }
      });

      expect(res.status).toEqual(500);
    });
  });
});
