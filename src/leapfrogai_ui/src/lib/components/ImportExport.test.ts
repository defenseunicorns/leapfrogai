import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import ImportExport from '$components/ImportExport.svelte';
import { vi } from 'vitest';
import { toastStore } from '$stores';
import { getFakeConversation } from '../../testUtils/fakeData';
import { mockNewConversationError } from '$lib/mocks/chat-mocks';

const uploadJSONFile = async (obj: object) => {
	const dataStr = JSON.stringify(obj);

	const blob = new Blob([dataStr]);
	const file = new File([blob], 'badData.json', { type: 'application/JSON' });
	File.prototype.text = vi.fn().mockResolvedValueOnce(dataStr);
	const uploadBtn = screen.getByLabelText(/import data/i);

	await userEvent.upload(uploadBtn, file);
};

describe('Import and Export data', () => {
	// Note - actual exporting and importing of data tested with E2E test

	it('displays a toast error if the imported data is in an invalid format', async () => {
		const toastSpy = vi.spyOn(toastStore, 'addToast');
		render(ImportExport);

		const badData = { improper: 'format' };

		await uploadJSONFile(badData);

		await waitFor(() => expect(toastSpy).toHaveBeenCalledTimes(1));
		expect(toastSpy).toHaveBeenCalledWith({
			kind: 'error',
			title: 'Error',
			subtitle: `Conversations are incorrectly formatted.`
		});
	});

	it('displays a toast error if their is an error while storing the imported data', async () => {
		mockNewConversationError();

		const toastSpy = vi.spyOn(toastStore, 'addToast');
		render(ImportExport);

		const data = getFakeConversation();

		await uploadJSONFile([data]);

		await waitFor(() => expect(toastSpy).toHaveBeenCalledTimes(1));
		expect(toastSpy).toHaveBeenCalledWith({
			kind: 'error',
			title: 'Error',
			subtitle: `Error importing conversation: ${data.label}`
		});
	});

	it('displays a toast error if there is an error exporting data', async () => {
		const toastSpy = vi.spyOn(toastStore, 'addToast');

		const originalEncode = encodeURIComponent;

		// @ts-ignore
		encodeURIComponent = vi.fn(() => {
			throw new Error('error');
		});
		render(ImportExport);

		await userEvent.click(screen.getByText('Export data'));
		expect(toastSpy).toHaveBeenCalledTimes(1);
		expect(toastSpy).toHaveBeenCalledWith({
			kind: 'error',
			title: 'Error',
			subtitle: `Error exporting conversations.`
		});

		// Restore
		// @ts-ignore
		encodeURIComponent = originalEncode;
	});

	it("only allows uploading of JSON files", async () => {
		render(ImportExport);
		const uploadBtn = screen.getByLabelText(/import data/i);

		expect(uploadBtn).toHaveAttribute('accept', 'application/json')
	})
});
