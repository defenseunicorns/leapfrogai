import { render, screen } from '@testing-library/svelte';
import { afterAll, afterEach, type MockInstance, vi } from 'vitest';
import { Message } from '$components/index';
import userEvent from '@testing-library/user-event';
import { getFakeMessage } from '$testUtils/fakeData';
import MessageWithToast from '$components/MessageWithToast.test.svelte';
import { convertMessageToAiMessage, getMessageText } from '$helpers/threads';
import { type Message as AIMessage } from 'ai/svelte';
import * as chatHelpers from '$helpers/chatHelpers';

const fakeAppend = vi.fn();
const fakeReload = vi.fn();

const getDefaultMessageProps = () => {
  let messages: AIMessage[] = [];
  const setMessages = (newMessages: AIMessage[]) => {
    messages = [...newMessages];
  };
  return {
    message: convertMessageToAiMessage(getFakeMessage()),
    messages,
    setMessages,
    isLastMessage: false,
    isLoading: false,
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
      message: convertMessageToAiMessage(fakeMessage)
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
      .spyOn(chatHelpers, 'handleChatMessageEdit')
      .mockImplementationOnce(vi.fn());

    const fakeMessage = getFakeMessage();
    render(Message, {
      ...getDefaultMessageProps(),
      message: convertMessageToAiMessage(fakeMessage)
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
      message: convertMessageToAiMessage(fakeAssistantMessage)
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
        message: convertMessageToAiMessage(fakeAssistantMessage)
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
        message: convertMessageToAiMessage(fakeAssistantMessage)
      });

      await userEvent.click(screen.getByLabelText('copy message'));

      await screen.findByText('Error copying text.');
    });

    it('disables edit submit button when message is loading', async () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        isLoading: true
      });

      const editPromptBtn = screen.getByLabelText('edit prompt');
      await userEvent.click(editPromptBtn);

      const submitBtn = screen.getByRole('button', { name: /submit/i });
      expect(submitBtn).toHaveProperty('disabled', true);
    });
    it('has copy and regenerate buttons for the last AI response', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToAiMessage(getFakeMessage({ role: 'assistant' })),
        isLastMessage: true
      });

      expect(screen.getByLabelText('copy message'));
      expect(screen.getByLabelText('regenerate message'));
    });
    it('does not have regenerate buttons for user messages', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToAiMessage(getFakeMessage({ role: 'user' })),
        isLastMessage: true
      });

      expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
    });
    it('does not have regenerate buttons for AI responses that are not the last response', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToAiMessage(getFakeMessage({ role: 'assistant' })),
        isLastMessage: false
      });

      expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
    });
    it('does not have a copy button for user messages', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToAiMessage(getFakeMessage({ role: 'user' }))
      });

      expect(screen.queryByLabelText('copy message')).not.toBeInTheDocument();
    });
    it('removes the copy and regenerate buttons when a response is loading', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToAiMessage(getFakeMessage({ role: 'assistant' })),
        isLastMessage: true,
        isLoading: true
      });
      expect(screen.queryByLabelText('copy message')).not.toBeInTheDocument();
      expect(screen.queryByLabelText('regenerate message')).not.toBeInTheDocument();
    });
    it('leaves the copy button for messages when it is loading if not the latest message', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToAiMessage(getFakeMessage({ role: 'assistant' })),
        isLastMessage: false,
        isLoading: true
      });
      expect(screen.getByLabelText('copy message')).toBeInTheDocument();
    });
    it('leaves the edit button for messages when it is loading if not the latest message', () => {
      render(MessageWithToast, {
        ...getDefaultMessageProps(),
        message: convertMessageToAiMessage(getFakeMessage({ role: 'user' })),
        isLastMessage: false,
        isLoading: true
      });
      screen.getByLabelText('edit prompt');
    });
  });
});
