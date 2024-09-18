import FileChatActions from '$components/FileChatActions.svelte';
import { render, screen } from '@testing-library/svelte';
import type { FileMetadata, LFFile } from '$lib/types/files';
import userEvent from '@testing-library/user-event';
import { mockConvertFileNoId } from '$lib/mocks/file-mocks';
import { mockNewMessage, mockTranslation, mockTranslationError } from '$lib/mocks/chat-mocks';
import { vi } from 'vitest';
import { toastStore } from '$stores';
import { FILE_TRANSLATION_ERROR } from '$constants/toastMessages';

const mockFile1: LFFile = new File([], 'test1.mpeg', { type: 'audio/mpeg' });
const mockFile2: LFFile = new File([], 'test1.mp4', { type: 'audio/mp4' });

mockFile1.id = '1';
mockFile2.id = '2';

const mockMetadata1: FileMetadata = {
  id: mockFile1.id,
  name: mockFile1.name,
  type: 'audio/mpeg',
  status: 'complete',
  text: ''
};

const mockMetadata2: FileMetadata = {
  id: mockFile2.id,
  name: mockFile2.name,
  type: 'audio/mp4',
  status: 'complete',
  text: ''
};

describe('FileChatActions', () => {
  it('should render a translate button for each audio file', () => {
    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: '123',
      originalMessages: [],
      setMessages: vi.fn()
    });

    expect(screen.getByText(`Translate ${mockMetadata1.name}`));
    expect(screen.getByText(`Translate ${mockMetadata2.name}`));
  });

  // Tests that correct endpoints are called when clicked
  // This is testing implementation rather than behavior, but is the best we can do for this component without
  // going up a level for a complicated integration test (behavior is tested in e2e)
  it('creates a message and requests a translation for the user requesting translation', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch');

    mockConvertFileNoId('');
    mockNewMessage();
    mockTranslation();
    mockNewMessage();
    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: '123',
      originalMessages: [],
      setMessages: vi.fn()
    });

    await userEvent.click(screen.getByRole('button', { name: `Translate ${mockMetadata2.name}` }));
    expect(fetchSpy).toHaveBeenNthCalledWith(
      1,
      expect.stringContaining('/api/messages/new'),
      expect.any(Object)
    );
    expect(fetchSpy).toHaveBeenNthCalledWith(
      2,
      expect.stringContaining('/api/audio/translation'),
      expect.any(Object)
    );
    expect(fetchSpy).toHaveBeenNthCalledWith(
      3,
      expect.stringContaining('/api/messages/new'),
      expect.any(Object)
    );
  });

  it('dispatches a toast if there is an error translating a file', async () => {
    mockConvertFileNoId('');
    mockNewMessage();
    mockTranslationError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');

    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: '123',
      originalMessages: [],
      setMessages: vi.fn()
    });

    await userEvent.click(screen.getByRole('button', { name: `Translate ${mockMetadata2.name}` }));
    expect(toastSpy).toHaveBeenCalledWith(FILE_TRANSLATION_ERROR());
  });
});
