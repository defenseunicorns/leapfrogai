import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { afterAll, beforeAll, type MockInstance, vi } from 'vitest';
import * as navigation from '$app/navigation';
import { ASSISTANTS_DESCRIPTION_MAX_LENGTH, ASSISTANTS_NAME_MAX_LENGTH } from '$lib/constants';
import { actions as editActions, load as editLoad } from './edit/[assistantId]/+page.server';
import { actions as newActions, load as newLoad } from './new/+page.server';
import {
  storageRemoveMock,
  supabaseInsertSingleMock,
  supabaseStorageMockWrapper
} from '$lib/mocks/supabase-mocks';
import {
  getFakeAssistant,
  getFakeAssistantInput,
  getFakeFileObject,
  getFakeFiles,
  getFakeVectorStore,
  getFakeVectorStoreFile
} from '$testUtils/fakeData';
import AssistantForm from '$components/AssistantForm.svelte';
import { mockOpenAI } from '../../../../../vitest-setup';
import { mockGetAssistants } from '$lib/mocks/chat-mocks';
import { mockGetFiles } from '$lib/mocks/file-mocks';
import { getLocalsMock } from '$lib/mocks/misc';
import type { ActionFailure, RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';
import filesStore from '$stores/filesStore';
import { convertFileObjectToFileRows } from '$helpers/fileHelpers';
import vectorStatusStore from '$stores/vectorStatusStore';

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

  it("does not show a file if it's vector status is failed", async () => {
    /* --- SETUP
      This extensive setup is an example of why E2E tests are sometimes preferred to unit tests. In this situation,
      getting a vector file with status of 'failed' in an E2E is not feasible, so we have to unit test it
    --- */
    const files = getFakeFiles({ numFiles: 2 });
    const vectorStore = getFakeVectorStore();
    const vectorStoreFile1 = getFakeVectorStoreFile({
      id: files[0].id,
      vector_store_id: vectorStore.id
    });
    const vectorStoreFile2 = getFakeVectorStoreFile({
      id: files[1].id,
      vector_store_id: vectorStore.id
    });
    vectorStoreFile2.status = 'failed';

    const assistant = getFakeAssistant({ vectorStoreId: vectorStore.id });

    mockOpenAI.setVectorStoreFiles([vectorStoreFile1, vectorStoreFile2]);
    mockOpenAI.setAssistants([assistant]);
    mockGetAssistants([]);
    mockGetFiles(files);
    filesStore.setFiles(convertFileObjectToFileRows(files));

    vectorStatusStore.set({
      [files[0].id]: { [vectorStore.id]: 'completed' },
      [files[1].id]: { [vectorStore.id]: 'failed' }
    });
    // @ts-expect-error: overcomplicated to mock out load function arguments and they are not used
    const data = await editLoad({ params: { assistantId: assistant.id }, locals: getLocalsMock() });
    /* --- END SETUP --- */

    render(AssistantForm, { data, isEditMode: true });
    screen.getByTestId(`${files[0].filename}-hide-uploader-item`);
    expect(screen.queryByTestId(`${files[1].filename}-hide-uploader-item`)).not.toBeInTheDocument();
  });

  it('has a cancel btn that navigates back to the management page', async () => {
    mockGetAssistants([]);
    mockGetFiles([]);

    // @ts-expect-error: overcomplicated to mock out load function arguments and they are not used
    const data = await newLoad();
    render(AssistantForm, { data });

    const cancelBtn = screen.getByTestId('assistant-form-cancel-btn');
    await userEvent.click(cancelBtn);

    expect(goToSpy).toHaveBeenCalledWith('/chat/assistants-management');
  });

  it('limits the name input length', async () => {
    mockGetAssistants([]);
    mockGetFiles([]);
    // @ts-expect-error: overcomplicated to mock out load function arguments and they are not used
    const data = await newLoad();
    render(AssistantForm, { data });
    const nameField = screen.getByRole('textbox', { name: /name/i });
    await userEvent.type(nameField, 'a'.repeat(ASSISTANTS_NAME_MAX_LENGTH + 1));
    expect(nameField).toHaveValue('a'.repeat(ASSISTANTS_NAME_MAX_LENGTH));
  });

  it('limits the description input length', async () => {
    mockGetAssistants([]);
    mockGetFiles([]);
    // @ts-expect-error: overcomplicated to mock out load function arguments and they are not used
    const data = await newLoad();
    render(AssistantForm, { data });
    const descriptionField = screen.getByRole('textbox', { name: /tagline/i });
    await userEvent.type(descriptionField, 'a'.repeat(ASSISTANTS_DESCRIPTION_MAX_LENGTH + 1));
    expect(descriptionField).toHaveValue('a'.repeat(ASSISTANTS_DESCRIPTION_MAX_LENGTH));
  });
  /* Note - instructions length limit is too long, test times out.
       Attempts to mock the constant required specifying each variable from the constants file in the mock
       (vi.importActual) did not work
       The extra maintenance overhead was deemed not worth testing this field
    */

  describe('the new assistant server side form action', () => {
    it('redirects on success (with data sources)', async () => {
      const fakeFile1 = getFakeFileObject();
      const fakeFile2 = getFakeFileObject();

      const assistant = getFakeAssistantInput();

      const formData = new FormData();
      formData.append('name', assistant.name!);
      formData.append('description', assistant.description!);
      formData.append('instructions', assistant.instructions!);
      formData.append('data_sources', `${fakeFile1.filename},${fakeFile2.filename}`);

      formData.append('pictogram', 'User');

      const request = new Request('http://localhost:5173/chat/assistants-management/new', {
        method: 'POST',
        body: formData
      });

      // Redirect from sveltekit throws
      try {
        await newActions.default({
          request,
          locals: getLocalsMock({ supabase: supabaseInsertSingleMock(assistant) })
        } as RequestEvent<RouteParams, '/chat/(settings)/assistants-management/new'>);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (redirect: any) {
        expect(redirect?.status).toEqual(303);
        expect(redirect?.location).toBe('/chat/assistants-management');
      }
    });

    it('returns a 401 if the request is unauthenticated', async () => {
      const request = new Request('http://localhost:5173/chat/assistants-management/new', {
        method: 'POST'
      });
      const res = (await newActions.default({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<
        RouteParams,
        '/chat/(settings)/assistants-management/new'
      >)) as ActionFailure;

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
    const res = (await newActions.default({
      request,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/chat/(settings)/assistants-management/new'>)) as ActionFailure;

    expect(res.status).toEqual(400);
  });

  describe('the edit assistant server side form action (with data sources)', () => {
    it('redirects on success', async () => {
      const fakeFile1 = getFakeFileObject();
      const fakeFile2 = getFakeFileObject();
      const assistant = getFakeAssistant();

      const formData = new FormData();
      formData.append('id', assistant.id!);
      formData.append('name', assistant.name!);
      formData.append('description', assistant.description!);
      formData.append('instructions', assistant.instructions!);
      formData.append('data_sources', `${fakeFile1.filename},${fakeFile2.filename}`);
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
          locals: getLocalsMock({
            supabase: supabaseStorageMockWrapper({
              ...storageRemoveMock()
            })
          })
        } as RequestEvent<
          RouteParams & { assistantId: string },
          '/chat/(settings)/assistants-management/edit/[assistantId]'
        >);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (redirect: any) {
        expect(redirect?.status).toEqual(303);
        expect(redirect?.location).toBe('/chat/assistants-management');
      }
    });

    it('returns a 401 if the request is unauthenticated', async () => {
      const request = new Request(`http://localhost:5173/chat/assistants-management/edit/123`, {
        method: 'POST'
      });
      const res = (await editActions.default({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<
        RouteParams & { assistantId: string },
        '/chat/(settings)/assistants-management/edit/[assistantId]'
      >)) as ActionFailure;

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

      const res = (await editActions.default({
        request,
        locals: getLocalsMock()
      } as RequestEvent<
        RouteParams & { assistantId: string },
        '/chat/(settings)/assistants-management/edit/[assistantId]'
      >)) as ActionFailure;

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
      const res = (await editActions.default({
        request,
        locals: getLocalsMock()
      } as RequestEvent<
        RouteParams & { assistantId: string },
        '/chat/(settings)/assistants-management/edit/[assistantId]'
      >)) as ActionFailure;

      expect(res.status).toEqual(500);
    });
  });
});
