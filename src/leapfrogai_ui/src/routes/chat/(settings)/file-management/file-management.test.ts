import { fireEvent, render, screen, waitFor } from '@testing-library/svelte';
import FileManagementPage from './+page.svelte';
import { getFakeAssistant, getFakeFiles } from '$testUtils/fakeData';
import userEvent from '@testing-library/user-event';
import { formatDate } from '$helpers/dates';
import { load } from './+page';
import {
  mockDeleteCheck,
  mockDeleteFile,
  mockDeleteFileWithDelay,
  mockGetFiles
} from '$lib/mocks/file-mocks';
import { vi } from 'vitest';
import { toastStore } from '$stores';

describe('file management', () => {
  it('lists all the files', async () => {
    const files = getFakeFiles();
    mockGetFiles(files);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });
    render(FileManagementPage, { data });

    files.forEach((file) => {
      expect(screen.getByText(file.filename));
    });
  });
  it('searches for files by filename', async () => {
    const files = getFakeFiles();
    mockGetFiles(files);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });
    render(FileManagementPage, { data });

    expect(screen.getByText(files[1].filename)).toBeInTheDocument();
    await userEvent.type(screen.getByRole('searchbox'), files[0].filename);
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

    mockGetFiles([file1, file2]);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });

    render(FileManagementPage, { data });

    expect(screen.getByText(file2.filename)).toBeInTheDocument();
    await userEvent.type(
      screen.getByRole('searchbox'),
      formatDate(new Date(file1.created_at * 1000))
    );
    expect(screen.queryByText(file2.filename)).not.toBeInTheDocument();
    expect(screen.getByText(file1.filename)).toBeInTheDocument();
  });

  it('confirms the files and affected assistants, then deletes them', async () => {
    const toastSpy = vi.spyOn(toastStore, 'addToast');
    const assistant1 = getFakeAssistant();
    const assistant2 = getFakeAssistant();
    const files = getFakeFiles();
    mockDeleteCheck([assistant1, assistant2]);
    mockDeleteFile();
    mockGetFiles(files);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });
    render(FileManagementPage, { data });

    const checkboxes = screen.getAllByRole('checkbox');

    await fireEvent.click(checkboxes[1]);
    await fireEvent.click(checkboxes[2]);

    expect(screen.getByText(files[0].filename)).toBeInTheDocument();
    expect(screen.getByText(files[1].filename)).toBeInTheDocument();

    const deleteBtns = screen.getAllByRole('button', { name: /delete/i });

    await userEvent.click(deleteBtns[0]);

    // Running deletion check
    expect(screen.getByText('Checking for any assistants affected by deletion...'));
    expect(deleteBtns[1]).toBeDisabled();
    await waitFor(() => expect(deleteBtns[1]).not.toBeDisabled());

    // Deletion check completed
    screen.getByText(/are you sure you want to delete \?/i);

    // Affected assistants displayed
    expect(screen.queryByText(assistant1.name!));
    expect(screen.queryByText(assistant2.name!));

    await waitFor(() => expect(deleteBtns[1]).not.toBeDisabled());
    await userEvent.click(deleteBtns[1]);

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'Files Deleted',
      subtitle: ''
    });
  });

  it('disables the delete button when there are no rows selected', async () => {
    // Note - the delete button is hidden when there are no rows selected, but still on the page so it needs to be
    // disabled
    const files = getFakeFiles();
    mockGetFiles(files);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });
    render(FileManagementPage, { data });

    const deleteBtn = screen.getAllByRole('button', { name: /delete/i })[0];
    expect(deleteBtn).toBeDisabled();
  });
  it('replaces the delete button with a loading spinner while deleting', async () => {
    mockDeleteCheck([]);
    mockDeleteFileWithDelay();
    const files = getFakeFiles();
    mockGetFiles(files);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });
    render(FileManagementPage, { data });

    const deleteBtns = screen.getAllByRole('button', { name: /delete/i });

    const checkboxes = screen.getAllByRole('checkbox');

    await fireEvent.click(checkboxes[1]); // select file
    expect(screen.queryByTestId('delete-pending')).not.toBeInTheDocument(); // no loading spinner yet
    await userEvent.click(deleteBtns[0]);
    await waitFor(() => expect(deleteBtns[1]).not.toBeDisabled());
    // Deletion check completed
    screen.getByText(/are you sure you want to delete \?/i);

    await userEvent.click(deleteBtns[1]); // confirm delete
    const deleteBtns2 = screen.getAllByRole('button', { name: /delete/i });
    expect(deleteBtns2).toHaveLength(1); // only modal delete btn remains in document
    expect(screen.queryByTestId('delete-pending')).toBeInTheDocument();
  });
  it("doesn't display warning about affected assistants when the file doesn't affect any assistants", async () => {
    const files = getFakeFiles();
    mockDeleteCheck([]); // no assistants affected
    mockGetFiles(files);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });
    render(FileManagementPage, { data });

    const checkboxes = screen.getAllByRole('checkbox');

    await fireEvent.click(checkboxes[1]);

    const deleteBtns = screen.getAllByRole('button', { name: /delete/i });

    await userEvent.click(deleteBtns[0]);

    // Running deletion check
    screen.getByText('Checking for any assistants affected by deletion...');
    expect(deleteBtns[1]).toBeDisabled();
    await waitFor(() => expect(deleteBtns[1]).not.toBeDisabled());

    // Deletion check completed
    screen.getByText(/are you sure you want to delete \?/i);

    expect(
      screen.queryByText(/this will affect the following assistants/i)
    ).not.toBeInTheDocument();
  });
});
