import { fireEvent, render, screen } from '@testing-library/svelte';
import FileManagementPage from './+page.svelte';
import { getFakeFiles } from '../../../../../testUtils/fakeData';
import userEvent from '@testing-library/user-event';
import { formatDate } from '$helpers/dates';
import { load } from './+page';
import { mockDeleteFile, mockDeleteFileWithDelay, mockGetFiles } from '$lib/mocks/file-mocks';
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

  it('deletes multiple files', async () => {
    const toastSpy = vi.spyOn(toastStore, 'addToast');
    mockDeleteFile();
    const files = getFakeFiles();
    mockGetFiles(files);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });
    render(FileManagementPage, { data });

    const checkboxes = screen.getAllByRole('checkbox');

    await fireEvent.click(checkboxes[0]);
    await fireEvent.click(checkboxes[1]);

    expect(screen.getByText(files[0].filename)).toBeInTheDocument();
    expect(screen.getByText(files[1].filename)).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: /delete/i }));

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'File Deleted',
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

    const deleteBtn = screen.getByRole('button', { name: /delete/i });
    expect(deleteBtn).toBeDisabled();
  });
  it('replaces the delete button with a loading spinner while deleting', async () => {
    mockDeleteFileWithDelay();
    const files = getFakeFiles();
    mockGetFiles(files);

    const data = await load({ fetch: global.fetch, depends: vi.fn() });
    render(FileManagementPage, { data });

    const deleteBtn = screen.getByRole('button', { name: /delete/i });

    const checkboxes = screen.getAllByRole('checkbox');

    await fireEvent.click(checkboxes[0]);
    expect(screen.queryByTestId('delete-pending')).not.toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: /delete/i }));
    expect(deleteBtn).not.toBeInTheDocument();
    expect(screen.queryByTestId('delete-pending')).toBeInTheDocument();
  });
});
