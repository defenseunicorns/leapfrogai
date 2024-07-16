import { render, screen } from '@testing-library/svelte';
import { afterAll, afterEach, type MockInstance, vi } from 'vitest';
import { Message } from '$components/index';
import userEvent from '@testing-library/user-event';
import { fakeAssistants, fakeThreads, getFakeMessage } from '$testUtils/fakeData';
import MessageWithToast from '$components/MessageWithToast.test.svelte';
import { convertMessageToVercelAiMessage, getMessageText } from '$helpers/threads';
import { type Message as VercelAIMessage } from '@ai-sdk/svelte';
import { chatHelpers } from '$helpers';
import { threadsStore } from '$stores';
import { NO_SELECTED_ASSISTANT_ID } from '$constants';

const fakeAppend = vi.fn();
const fakeReload = vi.fn();

const getDefaultMessageProps = () => {
  let messages: VercelAIMessage[] = [];
  const setMessages = (newMessages: VercelAIMessage[]) => {
    messages = [...newMessages];
  };
  return {
    allStreamedMessages: [],
    message: convertMessageToVercelAiMessage(getFakeMessage()),
    messages,
    setMessages,
    isLastMessage: false,
    append: fakeAppend,
    reload: fakeReload
  };
};

describe('Message component', () => {
  afterEach(() => {
    fakeAppend.mockReset();
    fakeReload.mockReset();
  });

  afterAll(() => {
    fakeAppend.mockRestore();
    fakeReload.mockRestore();
  });

  it('displays edit text area when edit btn is clicked', async () => {
    render(Message, { ...getDefaultMessageProps() });
    expect(screen.queryByText('edit message input')).not.toBeInTheDocument();
    const editPromptBtn = screen.getByLabelText('edit prompt');
    await userEvent.click(editPromptBtn);
    await screen.findByLabelText('edit message input');
  });
  it('removes the edit textarea and restores original text on close', async () => {
    const fakeMessage = getFakeMessage();
    render(Message, {
      ...getDefaultMessageProps(),
      message: convertMessageToVercelAiMessage(fakeMessage)
    });
    const editPromptBtn = screen.getByLabelText('edit prompt');
    expect(screen.queryByText('edit message input')).not.toBeInTheDocument();
    expect(screen.getByText(getMessageText(fakeMessage))).toBeInTheDocument();
    await userEvent.click(editPromptBtn);

    const input = screen.getByRole('textbox', { name: /edit message input/i });
    await userEvent.clear(input);
    expect(screen.queryByText(getMessageText(fakeMessage))).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: /cancel/i }));
    expect(screen.getByText(getMessageText(fakeMessage))).toBeInTheDocument();
  });
  it('submits message edit when submit is clicked', async () => {
    const handleEditSpy = vi
      .spyOn(chatHelpers, 'handleMessageEdit')
      .mockImplementationOnce(vi.fn());

    const fakeMessage = getFakeMessage();
    render(Message, {
      ...getDefaultMessageProps(),
      message: convertMessageToVercelAiMessage(fakeMessage)
    });
    const editPromptBtn = screen.getByLabelText('edit prompt');
    expect(screen.queryByText('edit message input')).not.toBeInTheDocument();
    expect(screen.getByText(getMessageText(fakeMessage))).toBeInTheDocument();
    await userEvent.click(editPromptBtn);

    await userEvent.click(screen.getByRole('button', { name: /submit/i }));
    expect(handleEditSpy).toHaveBeenCalledTimes(1);
  });
  it('does not allow editing non user messages', () => {
    const fakeAssistantMessage = getFakeMessage({ role: 'assistant' });
    render(Message, {
      ...getDefaultMessageProps(),
      message: convertMessageToVercelAiMessage(fakeAssistantMessage)
    });
    expect(screen.queryByLabelText('edit prompt')).not.toBeInTheDocument();
  });

  describe('util functions', () => {
    let clipboardSpy: MockInstance;

    afterAll(() => {
      clipboardSpy.mockRestore();
    });

    it('copies text of AI response to clipboard and sends a toast notification', async () => {
      Object.assign(navigator, {
        clipboard: { writeText: vi.fn().mockImplementation(() => Promise.resolve()) }
      });

      clipboardSpy = vi.spyOn(navigator.clipboard, 'writeText');
      const fakeAssistantMessage = getFakeMessage({ role: 'assistant' });
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(fakeAssistantMessage)
      });

      await userEvent.click(screen.getByLabelText('copy message'));

      expect(clipboardSpy).toHaveBeenCalledTimes(1);
      expect(clipboardSpy).toHaveBeenCalledWith(getMessageText(fakeAssistantMessage));
      await screen.findByText('Response message copied.');
    });
    it('sends an error toast notification if there is an error copying text', async () => {
      Object.assign(navigator, {
        clipboard: { writeText: vi.fn().mockImplementation(() => Promise.reject()) }
      });

      clipboardSpy = vi.spyOn(navigator.clipboard, 'writeText');
      const fakeAssistantMessage = getFakeMessage({ role: 'assistant' });
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(fakeAssistantMessage)
      });

      await userEvent.click(screen.getByLabelText('copy message'));

      await screen.findByText('Error copying text.');
    });

    it('disables edit submit button when message is loading', async () => {
      threadsStore.set({
        threads: fakeThreads,
        selectedAssistantId: NO_SELECTED_ASSISTANT_ID,
        sendingBlocked: true,
        lastVisitedThreadId: ''
      });
      render(MessageWithToast, {
        ...getDefaultMessageProps()
      });

      const editPromptBtn = screen.getByLabelText('edit prompt');
      await userEvent.click(editPromptBtn);

      const submitBtn = screen.getByRole('button', { name: /submit/i });
      expect(submitBtn).toHaveProperty('disabled', true);
    });
    it('has copy and regenerate buttons for the last AI response', () => {
      threadsStore.set({
        threads: fakeThreads,
        selectedAssistantId: NO_SELECTED_ASSISTANT_ID,
        sendingBlocked: false,
        lastVisitedThreadId: ''
      });
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(getFakeMessage({ role: 'assistant' })),
        isLastMessage: true
      });

      expect(screen.getByLabelText('copy message'));
      expect(screen.getByLabelText('regenerate message'));
    });
    it('does not have regenerate buttons for user messages', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(getFakeMessage({ role: 'user' })),
        isLastMessage: true
      });

      expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
    });
    it('does not have regenerate buttons for AI responses that are not the last response', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(getFakeMessage({ role: 'assistant' })),
        isLastMessage: false
      });

      expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
    });
    it('does not have a copy button for user messages', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(getFakeMessage({ role: 'user' }))
      });

      expect(screen.queryByLabelText('copy message')).not.toBeInTheDocument();
    });
    it('removes the regenerate buttons when a response is loading', () => {
      threadsStore.set({
        threads: fakeThreads,
        selectedAssistantId: NO_SELECTED_ASSISTANT_ID,
        sendingBlocked: true,
        lastVisitedThreadId: ''
      });
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(getFakeMessage({ role: 'assistant' })),
        isLastMessage: true
      });
      expect(screen.queryByLabelText('copy message')).toBeInTheDocument();
      expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
    });
    it('leaves the copy button for messages when it is loading', () => {
      threadsStore.set({
        threads: fakeThreads,
        selectedAssistantId: NO_SELECTED_ASSISTANT_ID,
        sendingBlocked: true,
        lastVisitedThreadId: ''
      });
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(getFakeMessage({ role: 'assistant' })),
        isLastMessage: false
      });
      expect(screen.getByLabelText('copy message')).toBeInTheDocument();
    });
    it('leaves the edit button for messages when it is loading', () => {
      threadsStore.set({
        threads: fakeThreads,
        selectedAssistantId: NO_SELECTED_ASSISTANT_ID,
        sendingBlocked: true,
        lastVisitedThreadId: ''
      });
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToVercelAiMessage(getFakeMessage({ role: 'user' })),
        isLastMessage: false
      });
      screen.getByLabelText('edit prompt');
    });
    it("Has the title 'You' for user messages", () => {
      render(Message, {
        ...getDefaultMessageProps(),
        message: getFakeMessage({ role: 'user' })
      });
      screen.getByText('You');
    });
    it("Has the title 'LeapfrogAI Bot' for regular AI responses", () => {
      render(Message, {
        ...getDefaultMessageProps(),
        message: getFakeMessage({ role: 'assistant', assistant_id: '123' })
      });
      screen.getByText('LeapfrogAI Bot');
    });
    it('Has the title of the assistant name for regular AI responses', () => {
      render(Message, {
        ...getDefaultMessageProps(),
        message: getFakeMessage({ role: 'assistant', assistant_id: fakeAssistants[0].id })
      });
      screen.getByText(fakeAssistants[0].name!);
    });
  });
});
