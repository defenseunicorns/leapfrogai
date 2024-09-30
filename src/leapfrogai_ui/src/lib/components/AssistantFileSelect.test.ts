import { filesStore } from '$stores';
import { render, screen } from '@testing-library/svelte';
import AssistantFileSelect from '$components/AssistantFileSelect.svelte';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { filesSchema } from '$schemas/files';
import type { LFFileObject } from '$lib/types/files';
import { getUnixSeconds } from '$helpers/dates';
import userEvent from '@testing-library/user-event';

const filesForm = await superValidate({}, yup(filesSchema), { errors: false });

describe('AssistantFileSelect', () => {
  const mockFiles: LFFileObject[] = [
    { id: '1', filename: 'file1.pdf', status: 'complete', created_at: getUnixSeconds(new Date()) },
    { id: '2', filename: 'file2.pdf', status: 'error', created_at: getUnixSeconds(new Date()) },
    { id: '3', filename: 'file3.txt', status: 'uploading', created_at: getUnixSeconds(new Date()) }
  ];

  beforeEach(() => {
    filesStore.set({
      files: mockFiles,
      selectedAssistantFileIds: ['1', '2'],
      uploading: false,
      selectedFileManagementFileIds: [],
      pendingUploads: []
    });
  });

  it('renders each selected file', async () => {
    render(AssistantFileSelect, {
      filesForm
    });

    expect(screen.getByTestId(`${mockFiles[0].filename}-${mockFiles[0].status}-uploader-item`));
    expect(screen.getByTestId(`${mockFiles[1].filename}-${mockFiles[1].status}-uploader-item`));
    expect(
      screen.queryByTestId(`${mockFiles[2].filename}-${mockFiles[2].status}-uploader-item`)
    ).not.toBeInTheDocument();
  });

  it('can select files', async () => {
    filesStore.set({
      files: mockFiles,
      selectedAssistantFileIds: [],
      uploading: false,
      selectedFileManagementFileIds: [],
      pendingUploads: []
    });

    render(AssistantFileSelect, {
      filesForm
    });

    expect(
      screen.queryByTestId(`${mockFiles[0].filename}-${mockFiles[0].status}-uploader-item`)
    ).not.toBeInTheDocument();

    await userEvent.click(screen.getByTestId('file-select-dropdown-btn'));
    await userEvent.click(screen.getByText(mockFiles[0].filename));
    screen.getByTestId(`${mockFiles[0].filename}-${mockFiles[0].status}-uploader-item`);
  });
});
