import { getFakeFiles } from '$testUtils/fakeData';
import {
  mockConvertFile,
  mockConvertFileError,
  mockGetFile,
  mockGetFileError
} from '$lib/mocks/file-mocks';
import Citation from '$components/Citation.svelte';
import { render, screen } from '@testing-library/svelte';
import { afterAll, beforeEach, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import { toastStore, uiStore } from '$stores';
import {
  CONVERT_FILE_ERROR_MSG_TOAST,
  FILE_DOWNLOAD_ERROR_MSG_TOAST,
  OPENAI_DOWNLOAD_DISABLED_MSG_TOAST
} from '$constants/toastMessages';

vi.mock('$app/environment', () => ({
  browser: true
}));

vi.stubGlobal('window', {
  ...window,
  open: vi.fn(),
  URL: {
    ...window.URL,
    createObjectURL: vi.fn(() => 'blob:http://localhost/file'),
    revokeObjectURL: vi.fn()
  },
  navigator: {
    clipboard: {
      writeText: vi.fn()
    }
  }
});

describe('Citation', () => {
  const toastSpy = vi.spyOn(toastStore, 'addToast');

  beforeEach(() => {
    uiStore.set({
      openSidebar: true,
      isUsingOpenAI: false
    });
  });

  afterAll(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('renders an iframe when a pdf is clicked', async () => {
    const file = getFakeFiles({ numFiles: 1 })[0];
    mockGetFile(file.id, 'test');

    render(Citation, { file, index: 1 });

    await userEvent.click(screen.getByTestId(`${file.id}-citation-btn`));
    await screen.findByTitle(`${file.id}-iframe`);
  });

  it('renders an iframe when a non-pdf file type is clicked (converted to pdf)', async () => {
    const file = getFakeFiles({ numFiles: 1 })[0];
    mockGetFile(file.id, 'test', 'text/plain');
    mockConvertFile(file.id, 'fake content');

    render(Citation, { file, index: 1 });

    await userEvent.click(screen.getByTestId(`${file.id}-citation-btn`));
    await screen.findByTitle(`${file.id}-iframe`);
  });

  it('shows a toast and does not render an iframe when OpenAI is being used', async () => {
    const file = getFakeFiles({ numFiles: 1 })[0];
    mockGetFile(file.id, 'test');
    uiStore.set({
      openSidebar: true,
      isUsingOpenAI: true
    });
    render(Citation, { file, index: 1 });

    await userEvent.click(screen.getByTestId(`${file.id}-citation-btn`));
    expect(screen.queryByTitle(`${file.id}-iframe`)).not.toBeInTheDocument();
    expect(toastSpy).toHaveBeenCalledWith({
      ...OPENAI_DOWNLOAD_DISABLED_MSG_TOAST()
    });
  });
  it('displays a toast when an error occurs after clicking a citation', async () => {
    const file = getFakeFiles({ numFiles: 1 })[0];
    mockGetFileError(file.id);

    render(Citation, { file, index: 1 });
    await userEvent.click(screen.getByTestId(`${file.id}-citation-btn`));

    expect(toastSpy).toHaveBeenCalledWith({
      ...FILE_DOWNLOAD_ERROR_MSG_TOAST()
    });
  });

  it('displays a toast when an error occurs when converting a file to pdf', async () => {
    const file = getFakeFiles({ numFiles: 1 })[0];
    mockGetFile(file.id, 'test', 'text/plain');
    mockConvertFileError(file.id);

    render(Citation, { file, index: 1 });
    await userEvent.click(screen.getByTestId(`${file.id}-citation-btn`));

    expect(toastSpy).toHaveBeenCalledWith({
      ...FILE_DOWNLOAD_ERROR_MSG_TOAST()
    });
  });
  it('displays a toast when the file type is not supported for download', async () => {
    const file = getFakeFiles({ numFiles: 1 })[0];
    mockGetFile(file.id, 'test', 'fakeFileType');

    render(Citation, { file, index: 1 });
    await userEvent.click(screen.getByTestId(`${file.id}-citation-btn`));

    expect(toastSpy).toHaveBeenCalledWith({
      ...CONVERT_FILE_ERROR_MSG_TOAST()
    });
  });
  it('open a new tab when the open in new tab button is clicked', async () => {
    const windowOpenSpy = vi.spyOn(window, 'open');
    const file = getFakeFiles({ numFiles: 1 })[0];

    mockGetFile(file.id, 'test');

    render(Citation, { file, index: 1 });

    await userEvent.click(screen.getByTestId(`${file.id}-citation-btn`));
    await screen.findByTitle(`${file.id}-iframe`);
    await userEvent.click(screen.getByTestId(`file-${file.id}-open-new-tab-btn`));
    expect(windowOpenSpy).toHaveBeenCalledTimes(1);
    expect(windowOpenSpy).toHaveBeenCalledWith('blob:http://localhost/file', '_blank');
  });

  // Note - downloading of file tested via E2E
});
