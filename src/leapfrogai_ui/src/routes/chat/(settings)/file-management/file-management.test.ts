import { render, screen } from '@testing-library/svelte';
import FileManagementPage from './+page.svelte';
import { getFakeFiles } from '../../../../../testUtils/fakeData';
import userEvent from "@testing-library/user-event";

describe('file management', () => {
  it('lists all the files', () => {
    const files = getFakeFiles();
    render(FileManagementPage, { data: { files } });

    files.forEach((file) => {
      expect(screen.getByText(file.filename));
    });
  });
  it("searches for files", async () => {
    const files = getFakeFiles();
    render(FileManagementPage, { data: { files } });

    await userEvent.type(screen.getByRole('searchbox'))
  })
});
