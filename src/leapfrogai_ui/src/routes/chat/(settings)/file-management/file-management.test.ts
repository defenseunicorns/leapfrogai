import { render, screen } from '@testing-library/svelte';
import FileManagementPage from './+page.svelte';
import { getFakeFiles } from '../../../../../testUtils/fakeData';
import userEvent from '@testing-library/user-event';
import { formatDate } from '$helpers/dates';

describe('file management', () => {
  it('lists all the files', () => {
    const files = getFakeFiles();
    render(FileManagementPage, { data: { files } });

    files.forEach((file) => {
      expect(screen.getByText(file.filename));
    });
  });
  it('searches for files by filename', async () => {
    const files = getFakeFiles();
    render(FileManagementPage, { data: { files } });

    expect(screen.getByText(files[1].filename)).toBeInTheDocument();
    await userEvent.type(screen.getByRole('searchbox'), files[0].filename);
    expect(screen.queryByText(files[1].filename)).not.toBeInTheDocument();
    expect(screen.getByText(files[0].filename)).toBeInTheDocument();
  });
  it('searches for files by filename', async () => {
    const currentDate = new Date();
    const yesterday = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth(),
      currentDate.getDate() - 1
    );

    const file1 = getFakeFiles({ numFiles: 1 })[0];
    const file2 = getFakeFiles({ numFiles: 1, created_at: yesterday })[0];

    render(FileManagementPage, { data: { files: [file1, file2] } });

    expect(screen.getByText(file2.filename)).toBeInTheDocument();
    await userEvent.type(
      screen.getByRole('searchbox'),
      formatDate(new Date(file1.created_at * 1000))
    );
    expect(screen.queryByText(file2.filename)).not.toBeInTheDocument();
    expect(screen.getByText(file1.filename)).toBeInTheDocument();
  });
});
