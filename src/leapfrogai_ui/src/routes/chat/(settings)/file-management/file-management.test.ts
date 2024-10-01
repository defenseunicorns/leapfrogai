import { fireEvent, render, screen, within } from '@testing-library/svelte';
import FileManagementPage from './+page.svelte';
import { getFakeAssistant, getFakeFiles, getFakeSession } from '$testUtils/fakeData';
import userEvent from '@testing-library/user-event';
import { formatDate } from '$helpers/dates';
import { load } from './+page';
import {
  mockDeleteCheck,
  mockDeleteFile,
  mockDeleteFileWithDelay,
  mockDownloadError,
  mockGetFiles
} from '$lib/mocks/file-mocks';
import { beforeEach, vi } from 'vitest';
import { filesStore, toastStore } from '$stores';
import { convertFileObjectToLFFileObject } from '$helpers/fileHelpers';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { filesSchema } from '$schemas/files';
import type { SupabaseClient } from '@supabase/supabase-js';
import type { FilesForm } from '$lib/types/files';
import { tick } from 'svelte';
import vectorStatusStore from '$stores/vectorStatusStore';

describe('file management', () => {
  const files = getFakeFiles();
  let form: FilesForm;
  let searchbox: HTMLElement;

  beforeEach(async () => {
    // @ts-expect-error: full mocking of load function params not necessary and is overcomplicated
    const data = await load();

    form = await superValidate(yup(filesSchema));
    filesStore.setFiles(convertFileObjectToLFFileObject(files));
    filesStore.setSelectedFileManagementFileIds([]);

    render(FileManagementPage, {
      data: {
        ...data,
        form,
        session: getFakeSession(),
        supabase: {} as unknown as SupabaseClient
      }
    });
    searchbox = screen.getByRole('textbox', {
      name: /search/i
    });
  });
  it('lists all the files', async () => {
    mockGetFiles(files);

    files.forEach((file) => {
      expect(screen.getByText(file.filename));
    });
  });
  it('searches for files by filename', async () => {
    mockGetFiles(files);

    expect(screen.getByText(files[1].filename)).toBeInTheDocument();
    await userEvent.type(searchbox, files[0].filename);
    expect(screen.queryByText(files[1].filename)).not.toBeInTheDocument();
    expect(screen.getByText(files[0].filename)).toBeInTheDocument();
  });
  it('searches for files by date', async () => {
    const currentDate = new Date();
    const yesterday = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth(),
      currentDate.getDate() - 1
    );

    const file1 = getFakeFiles({ numFiles: 1 })[0];
    const file2 = getFakeFiles({ numFiles: 1, created_at: yesterday })[0];

    // Set different files for this test, await tick so component reflect store update
    filesStore.setFiles(convertFileObjectToLFFileObject([file1, file2]));
    await tick();
    mockGetFiles([file1, file2]);

    expect(screen.getByText(file2.filename)).toBeInTheDocument();
    await userEvent.type(searchbox, formatDate(new Date(file1.created_at * 1000)));
    expect(screen.queryByText(file2.filename)).not.toBeInTheDocument();
    expect(screen.getByText(file1.filename)).toBeInTheDocument();
  });

  it('confirms the files and affected assistants, then deletes them', async () => {
    const vectorStatusStoreSpy = vi.spyOn(vectorStatusStore, 'removeFiles');
    const assistant1 = getFakeAssistant();
    const assistant2 = getFakeAssistant();
    const toastSpy = vi.spyOn(toastStore, 'addToast');
    mockDeleteFile();
    mockGetFiles(files);
    mockDeleteCheck([assistant1, assistant2]);

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await fireEvent.click(checkbox);

    expect(screen.getByText(files[0].filename)).toBeInTheDocument();
    expect(screen.getByText(files[1].filename)).toBeInTheDocument();

    const deleteBtn = screen.getByRole('button', { name: /delete/i });

    await userEvent.click(deleteBtn);

    // Running deletion check
    const modal = screen.getByTestId('delete-files-modal');
    const confirmDeleteBtn = within(modal).getByRole('button', { name: /delete/i });
    expect(screen.getByText('Checking for any assistants affected by deletion...'));
    expect(confirmDeleteBtn).toBeDisabled();

    // Deletion check completed
    await screen.findByText(/are you sure you want to delete \?/i);

    // Affected assistants displayed
    expect(screen.queryByText(assistant1.name!));
    expect(screen.queryByText(assistant2.name!));

    expect(confirmDeleteBtn).not.toBeDisabled();
    await userEvent.click(confirmDeleteBtn);

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'Files Deleted'
    });
    expect(vectorStatusStoreSpy).toHaveBeenCalledWith(files.map((file) => file.id));
  });

  it('replaces the delete button with a disabled loading spinner button while deleting', async () => {
    mockGetFiles(files);
    mockDeleteCheck([]);
    mockDeleteFileWithDelay();

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await userEvent.click(checkbox);
    const deleteBtn = screen.getByRole('button', { name: /delete/i });
    await userEvent.click(deleteBtn);
    const modal = screen.getByTestId('delete-files-modal');
    // Deletion check completed
    await screen.findByText(/are you sure you want to delete \?/i);

    await userEvent.click(within(modal).getByRole('button', { name: /delete/i }));

    expect(deleteBtn).not.toBeInTheDocument();
    const deleteSpinnerBtn = screen.getByRole('button', { name: /deleting/i });
    expect(deleteSpinnerBtn).toBeInTheDocument();
    expect(deleteSpinnerBtn).toBeDisabled();
    screen.getByText('Deleting...');
  });

  it("doesn't display warning about affected assistants when the file doesn't affect any assistants", async () => {
    mockDeleteCheck([]); // no assistants affected
    mockGetFiles(files);

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await fireEvent.click(checkbox);

    const deleteBtn = screen.getByRole('button', { name: /delete/i });

    await userEvent.click(deleteBtn);

    // Running deletion check
    await screen.findByText('Checking for any assistants affected by deletion...');

    // Deletion check completed
    await screen.findByText(/are you sure you want to delete \?/i);

    expect(
      screen.queryByText(/this will affect the following assistants/i)
    ).not.toBeInTheDocument();
  });

  it('displays an error toast when there is an error downloading a file', async () => {
    vi.mock('$app/environment', () => ({
      browser: true
    }));
    const toastSpy = vi.spyOn(toastStore, 'addToast');
    mockDeleteCheck([]); // no assistants affected
    mockGetFiles(files);
    for (const file of files) {
      mockDownloadError(file.id);
    }

    const checkbox = screen.getByRole('checkbox', {
      name: /select all rows/i
    });
    await fireEvent.click(checkbox);

    const downloadBtn = screen.getByRole('button', { name: /download/i });

    await userEvent.click(downloadBtn);
    files.forEach(() => {
      expect(toastSpy).toHaveBeenCalledWith({
        kind: 'error',
        title: 'Download Failed',
        subtitle: undefined // currentFilename is undefined since we don't get that far
      });
    });
  });
});

// TODO - The API Keys table also uses this pagination logic, but we are only testing it here on the files table
// Eventually we should refactor the table to a re-usable component and test there instead
// https://github.com/defenseunicorns/leapfrogai/issues/860
describe('table pagination', () => {
  const files = getFakeFiles({ numFiles: 15 });
  let form: FilesForm;
  let searchbox: HTMLElement;

  beforeEach(async () => {
    // @ts-expect-error: full mocking of load function params not necessary and is overcomplicated
    const data = await load();

    form = await superValidate(yup(filesSchema));
    filesStore.setFiles(convertFileObjectToLFFileObject(files));
    filesStore.setSelectedFileManagementFileIds([]);

    render(FileManagementPage, {
      data: {
        ...data,
        form,
        session: getFakeSession(),
        supabase: {} as unknown as SupabaseClient
      }
    });
    searchbox = screen.getByRole('textbox', {
      name: /search/i
    });
  });
  it('renders the correct item ranges', () => {
    mockGetFiles(files);
    expect(screen.getByText(/showing of entries/i));
    expect(screen.getByTestId('pagination-range').textContent).toEqual('1-10');
    expect(screen.getByTestId('pagination-total').textContent).toEqual('15');
  });

  it('renders 0 items when none found', async () => {
    mockGetFiles(files);

    await userEvent.type(searchbox, 'not an existing file');
    expect(screen.getByText(/showing entries/i));
    expect(screen.getByTestId('pagination-range').textContent).toEqual('0');
    expect(screen.queryByTestId('pagination-total')).not.toBeInTheDocument();
  });

  it('renders the correct item ranges when clicking next and prev', async () => {
    mockGetFiles(files);
    await userEvent.click(screen.getByTestId('next-btn'));
    expect(screen.getByText(/showing of entries/i));
    expect(screen.getByTestId('pagination-range').textContent).toEqual('11-15');
    expect(screen.getByTestId('pagination-total').textContent).toEqual('15');

    await userEvent.click(screen.getByTestId('prev-btn'));
    expect(screen.getByText(/showing of entries/i));
    expect(screen.getByTestId('pagination-range').textContent).toEqual('1-10');
    expect(screen.getByTestId('pagination-total').textContent).toEqual('15');
  });
  it('updates item counts when searching and switching pages', async () => {
    const searchTerm = files[0].filename;
    const filesThatMeetSearchCriteria = files.filter((file) => file.filename.includes(searchTerm));

    const searchbox = screen.getByRole('textbox', {
      name: /search/i
    });

    // Regular search
    await userEvent.type(searchbox, searchTerm);
    expect(screen.getByText(/showing of entries/i));
    expect(screen.getByTestId('pagination-range').textContent).toEqual(
      `1-${filesThatMeetSearchCriteria.length}`
    );
    expect(screen.getByTestId('pagination-total').textContent).toEqual(
      filesThatMeetSearchCriteria.length.toString()
    );

    // Clear search
    await userEvent.clear(searchbox);
    expect(screen.getByText(/showing of entries/i));
    expect(screen.getByTestId('pagination-range').textContent).toEqual('1-10');
    expect(screen.getByTestId('pagination-total').textContent).toEqual('15');

    // Search while on page 2
    await userEvent.click(screen.getByTestId('next-btn'));
    await userEvent.type(searchbox, searchTerm);
    expect(screen.getByText(/showing of entries/i));
    expect(screen.getByTestId('pagination-range').textContent).toEqual(
      `1-${filesThatMeetSearchCriteria.length}`
    );
    expect(screen.getByTestId('pagination-total').textContent).toEqual(
      filesThatMeetSearchCriteria.length.toString()
    );
  });
});
