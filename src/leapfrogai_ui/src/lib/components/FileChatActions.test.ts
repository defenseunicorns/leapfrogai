import FileChatActions from '$components/FileChatActions.svelte';
import { render, screen } from '@testing-library/svelte';
import type { FileMetadata, LFFile } from '$lib/types/files';
import userEvent from '@testing-library/user-event';
import { mockConvertFileNoId } from '$lib/mocks/file-mocks';
import {
  mockNewMessage,
  mockTranscription,
  mockTranscriptionError,
  mockTranscriptionFileSizeError,
  mockTranslation,
  mockTranslationError,
  mockTranslationFileSizeError
} from '$lib/mocks/chat-mocks';
import { vi } from 'vitest';
import { threadsStore, toastStore } from '$stores';
import {
  AUDIO_FILE_SIZE_ERROR_TOAST,
  FILE_TRANSCRIPTION_ERROR,
  FILE_TRANSLATION_ERROR
} from '$constants/toastMessages';
import { getFakeThread } from '$testUtils/fakeData';
import { NO_SELECTED_ASSISTANT_ID } from '$constants';

const thread = getFakeThread();

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
  beforeEach(() => {
    threadsStore.set({
      threads: [thread], // uses date override starting in March
      sendingBlocked: false,
      selectedAssistantId: NO_SELECTED_ASSISTANT_ID,
      lastVisitedThreadId: '',
      streamingMessage: null
    });
  });

  it('should render a translate and transcribe button for each audio file', () => {
    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: thread.id,
      originalMessages: [],
      setMessages: vi.fn()
    });

    expect(screen.getByText(`Translate ${mockMetadata1.name}`));
    expect(screen.getByText(`Translate ${mockMetadata2.name}`));

    expect(screen.getByText(`Transcribe ${mockMetadata1.name}`));
    expect(screen.getByText(`Transcribe ${mockMetadata2.name}`));
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
      threadId: thread.id,
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

  it('creates a message and requests a translation for the user requesting transcription', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch');

    mockConvertFileNoId('');
    mockNewMessage();
    mockTranscription();
    mockNewMessage();
    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: thread.id,
      originalMessages: [],
      setMessages: vi.fn()
    });

    await userEvent.click(screen.getByRole('button', { name: `Transcribe ${mockMetadata2.name}` }));
    expect(fetchSpy).toHaveBeenNthCalledWith(
      1,
      expect.stringContaining('/api/messages/new'),
      expect.any(Object)
    );
    expect(fetchSpy).toHaveBeenNthCalledWith(
      2,
      expect.stringContaining('/api/audio/transcription'),
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
      threadId: thread.id,
      originalMessages: [],
      setMessages: vi.fn()
    });

    await userEvent.click(screen.getByRole('button', { name: `Translate ${mockMetadata2.name}` }));
    expect(toastSpy).toHaveBeenCalledWith(FILE_TRANSLATION_ERROR());
  });
  it('dispatches a toast if there is an error transcribing a file', async () => {
    mockConvertFileNoId('');
    mockNewMessage();
    mockTranscriptionError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');

    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: thread.id,
      originalMessages: [],
      setMessages: vi.fn()
    });

    await userEvent.click(screen.getByRole('button', { name: `Transcribe ${mockMetadata2.name}` }));
    expect(toastSpy).toHaveBeenCalledWith(FILE_TRANSCRIPTION_ERROR());
  });

  it('dispatches a toast if the file for translation is too big', async () => {
    mockConvertFileNoId('');
    mockNewMessage();
    mockTranslationFileSizeError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');

    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: thread.id,
      originalMessages: [],
      setMessages: vi.fn()
    });

    await userEvent.click(screen.getByRole('button', { name: `Translate ${mockMetadata2.name}` }));
    expect(toastSpy).toHaveBeenCalledWith(AUDIO_FILE_SIZE_ERROR_TOAST());
  });

  it('dispatches a toast if the file for transcription is too big', async () => {
    mockConvertFileNoId('');
    mockNewMessage();
    mockTranscriptionFileSizeError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');

    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: thread.id,
      originalMessages: [],
      setMessages: vi.fn()
    });

    await userEvent.click(screen.getByRole('button', { name: `Transcribe ${mockMetadata2.name}` }));
    expect(toastSpy).toHaveBeenCalledWith(AUDIO_FILE_SIZE_ERROR_TOAST());
  });

  it('disables all buttons while a file is being processed, but only adds a spinner to the active action btn', async () => {
    mockConvertFileNoId('');
    mockNewMessage();
    mockTranslation({ delay: 50 });
    mockNewMessage();
    render(FileChatActions, {
      attachedFiles: [mockFile1, mockFile2],
      attachedFileMetadata: [mockMetadata1, mockMetadata2],
      threadId: thread.id,
      originalMessages: [],
      setMessages: vi.fn()
    });

    const file1TranslateBtn = screen.getByRole('button', {
      name: `Translate ${mockMetadata1.name}`
    });
    const file1TranscribeBtn = screen.getByRole('button', {
      name: `Transcribe ${mockMetadata1.name}`
    });
    const file2TranslateBtn = screen.getByRole('button', {
      name: `Translate ${mockMetadata2.name}`
    });
    const file2TranscribeBtn = screen.getByRole('button', {
      name: `Transcribe ${mockMetadata2.name}`
    });

    await userEvent.click(screen.getByRole('button', { name: `Translate ${mockMetadata1.name}` }));
    expect(screen.getByTestId('translation-spinner')).toBeInTheDocument();
    expect(screen.queryByTestId('transcription-spinner')).not.toBeInTheDocument();
    expect(file1TranslateBtn).toBeDisabled();
    expect(file1TranscribeBtn).toBeDisabled();
    expect(file2TranslateBtn).toBeDisabled();
    expect(file2TranscribeBtn).toBeDisabled();
  });
});
