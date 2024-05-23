import { fireEvent, render, screen, waitFor } from '@testing-library/svelte';
import FileManagementPage from './+page.svelte';
import { getFakeFiles } from '../../../../../testUtils/fakeData';
import userEvent from '@testing-library/user-event';
import { formatDate } from '$helpers/dates';
import { load } from './+page.server';
import { sessionMock } from '$lib/mocks/supabase-mocks';
import { mockOpenAI } from '../../../../../vitest-setup';
import { mockDeleteFile } from '$lib/mocks/chat-mocks';
import { vi } from 'vitest';
import { toastStore } from '$stores';

describe('file management', () => {
  it('lists all the files', async () => {
    const files = getFakeFiles();
    mockOpenAI.setFiles(files);

    const data = await load({ locals: { getSession: sessionMock } });
    render(FileManagementPage, { data });

    files.forEach((file) => {
      expect(screen.getByText(file.filename));
    });
  });
  it('searches for files by filename', async () => {
    const files = getFakeFiles();
    mockOpenAI.setFiles(files);

    const data = await load({ locals: { getSession: sessionMock } });
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

    mockOpenAI.setFiles([file1, file2]);

    const data = await load({ locals: { getSession: sessionMock } });

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
    mockOpenAI.setFiles(files);

    const data = await load({ locals: { getSession: sessionMock } });
    render(FileManagementPage, { data });

    const settingsBtn = screen.getByTestId('file-management-settings');
    await userEvent.click(settingsBtn);

    await userEvent.click(screen.getByRole('menuitem', { name: /edit/i }));
    const checkboxes = screen.getAllByRole('checkbox');

    await fireEvent.click(checkboxes[0]);
    await fireEvent.click(checkboxes[1]);

    expect(screen.getByText(files[0].filename)).toBeInTheDocument();
    expect(screen.getByText(files[1].filename)).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: /delete/i }));

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'success',
      title: 'Files deleted',
      subtitle: ''
    });
  });
});
