import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import ImportExport from '$components/ImportExport.svelte';
import { afterEach, vi } from 'vitest';
import { toastStore } from '$stores';
import { getFakeThread } from '$testUtils/fakeData';
import { mockNewThreadError } from '$lib/mocks/chat-mocks';

const uploadJSONFile = async (obj: object) => {
  const dataStr = JSON.stringify(obj);

  const blob = new Blob([dataStr]);
  const file = new File([blob], 'badData.json', { type: 'application/JSON' });
  File.prototype.text = vi.fn().mockResolvedValueOnce(dataStr);
  const uploadBtn = screen.getByTestId('import data input');

  await userEvent.upload(uploadBtn, file);
};

describe('Import and Export data', () => {
  // Note - actual exporting and importing of data tested with E2E test

  afterEach(() => {
    vi.restoreAllMocks;
  });

  it('displays a toast error if the imported data is in an invalid format', async () => {
    const toastSpy = vi.spyOn(toastStore, 'addToast');
    render(ImportExport);

    const badData = { improper: 'format' };

    await uploadJSONFile(badData);

    await waitFor(() => expect(toastSpy).toHaveBeenCalledTimes(2)); // first call is importing notification
    expect(toastSpy).toHaveBeenNthCalledWith(2, {
      kind: 'error',
      title: 'Error',
      subtitle: `Threads are incorrectly formatted.`
    });
  });

  it('displays a toast error if their is an error while storing the imported data', async () => {
    mockNewThreadError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');
    render(ImportExport);

    const data = getFakeThread();

    await uploadJSONFile([data]);

    await waitFor(() => expect(toastSpy).toHaveBeenCalledTimes(2));
    expect(toastSpy).toHaveBeenNthCalledWith(2, {
      kind: 'error',
      title: 'Error',
      subtitle: `Error importing thread: ${data.metadata.label}`
    });
  });

  it('displays a toast error if there is an error exporting data', async () => {
    const toastSpy = vi.spyOn(toastStore, 'addToast');

    vi.spyOn(window, 'encodeURIComponent').mockImplementation(() => {
      throw new Error('error');
    });

    render(ImportExport);

    await userEvent.click(screen.getByText('Export data'));
    expect(toastSpy).toHaveBeenCalledTimes(1);
    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'error',
      title: 'Error',
      subtitle: `Error exporting threads.`
    });
  });

  it('only allows uploading of JSON files', async () => {
    render(ImportExport);
    const uploadBtn = screen.getByTestId('import data input');

    expect(uploadBtn).toHaveAttribute('accept', 'application/json');
  });
});
