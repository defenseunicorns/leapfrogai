import Sidebar from '$components/LFSidebar.svelte';
import {
  mockDeleteThread,
  mockDeleteThreadError,
  mockEditThreadLabel,
  mockEditThreadLabelError
} from '$lib/mocks/chat-mocks';
import { threadsStore, toastStore } from '$stores';
import { fireEvent, render, screen, within } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { fakeThreads, getFakeThread } from '$testUtils/fakeData';
import { vi } from 'vitest';

import { getUnixSeconds, monthNames } from '$helpers/dates';
import * as navigation from '$app/navigation';
import { getMessageText } from '$helpers/threads';

const openThreadEditDeleteMenu = async (label: string) => {
  const sidebarThreadMenuBtn = screen.getByTestId(`thread-menu-btn-${label}`);
  await userEvent.click(sidebarThreadMenuBtn);
};

const clickEditThreadBtn = async () => {
  const editDeletePopover = screen.getByTestId('sidebar-popover');
  await userEvent.click(within(editDeletePopover).getByRole('button', { name: /edit/i }));
  expect(screen.getByTestId('edit-thread-input')).toBeInTheDocument();
};

const clickDeleteThreadBtn = async () => {
  const editDeletePopover = screen.getByTestId('sidebar-popover');
  await userEvent.click(within(editDeletePopover).getByRole('button', { name: /delete/i }));
};

const renameThread = async (oldLabel: string, newLabel: string, keyToPress = '{enter}') => {
  expect(screen.getByTestId('edit-thread-input')).toBeInTheDocument();
  const editInput = screen.getByDisplayValue(oldLabel); // also test input has original label
  await userEvent.clear(editInput);
  await userEvent.type(editInput, newLabel);
  await userEvent.keyboard(keyToPress);
};

const editThreadsLabel = async (oldLabel: string, newLabel: string, keyToPress = '{enter}') => {
  await openThreadEditDeleteMenu(fakeThreads[0].metadata.label);
  await clickEditThreadBtn();
  await renameThread(oldLabel, newLabel, keyToPress);
};

describe('ChatSidebar', () => {
  it('renders threads', async () => {
    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    const threadsSection = screen.getByTestId('threads');

    fakeThreads.forEach((thread) => {
      expect(
        within(threadsSection).getByRole('button', { name: thread.metadata.label })
      ).toBeInTheDocument();
    });
  });

  it('does not render date categories that have no threads', async () => {
    const today = new Date();
    const fakeTodayThread = getFakeThread();
    const fakeYesterdayThread = getFakeThread({
      created_at: getUnixSeconds(
        new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1)
      )
    });

    threadsStore.set({
      threads: [fakeTodayThread, fakeYesterdayThread], // uses date override starting in March
      sendingBlocked: false,
      lastVisitedThreadId: '',
      streamingMessage: null
    });

    render(Sidebar);
    const threadsSection = screen.getByTestId('threads');

    expect(
      within(threadsSection).getByRole('button', { name: fakeTodayThread.metadata.label })
    ).toBeInTheDocument();
    expect(
      within(threadsSection).getByRole('button', { name: fakeYesterdayThread.metadata.label })
    ).toBeInTheDocument();

    expect(screen.getByText('Today')).toBeInTheDocument();
    expect(screen.getByText('Yesterday')).toBeInTheDocument();

    expect(screen.queryByText(monthNames[today.getMonth()])).not.toBeInTheDocument();
    expect(screen.queryByText(monthNames[today.getMonth() - 1])).not.toBeInTheDocument();
  });

  it('deletes threads', async () => {
    mockDeleteThread();

    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();
    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[1].metadata.label })
    ).toBeInTheDocument();

    await openThreadEditDeleteMenu(fakeThreads[0].metadata.label);
    await clickDeleteThreadBtn();

    const modal = screen.getByTestId('delete-thread-modal');
    expect(modal).toBeVisible();

    const confirmDeleteBtn = within(modal).getByRole('button', { name: /delete/i });
    await userEvent.click(confirmDeleteBtn);
    expect(modal).not.toBeVisible;

    expect(
      within(threadsSection).queryByRole('button', { name: fakeThreads[0].metadata.label })
    ).not.toBeInTheDocument();
    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[1].metadata.label })
    ).toBeInTheDocument();
  });
  it('dispatches a toast when there is an error deleting a thread and it does not delete the thread from the screen', async () => {
    mockDeleteThreadError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');

    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();

    await openThreadEditDeleteMenu(fakeThreads[0].metadata.label);
    await clickDeleteThreadBtn();

    const modal = screen.getByTestId('delete-thread-modal');

    expect(modal).toBeVisible();

    const confirmDeleteBtn = within(modal).getByRole('button', { name: /delete/i });
    await userEvent.click(confirmDeleteBtn);

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();
    expect(toastSpy).toHaveBeenCalledTimes(1);
  });

  it('edits thread labels', async () => {
    const newLabelText = 'new label';
    mockEditThreadLabel();

    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText);
    expect(within(threadsSection).getByRole('button', { name: newLabelText })).toBeInTheDocument();
  });

  it('edits thread labels when tab is pressed instead of enter', async () => {
    const newLabelText = 'new label';
    mockEditThreadLabel();

    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText, '{Tab}');
    expect(within(threadsSection).getByRole('button', { name: newLabelText })).toBeInTheDocument();
  });

  it('edits thread labels when the user clicks away from the input (onBlur)', async () => {
    const newLabelText = 'new label';
    mockEditThreadLabel();

    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();

    await openThreadEditDeleteMenu(fakeThreads[0].metadata.label);
    await clickEditThreadBtn();

    const editInput = screen.getByDisplayValue(fakeThreads[0].metadata.label);
    await userEvent.clear(editInput);
    await userEvent.type(editInput, newLabelText);

    await fireEvent.blur(editInput);
    await screen.findByRole('button', { name: newLabelText });
  });

  it('dispatches a toast when there is an error editing a threads label and it does not update the label on the screen', async () => {
    mockEditThreadLabelError();
    const toastSpy = vi.spyOn(toastStore, 'addToast');

    const newLabelText = 'new label';
    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText);

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();
    expect(toastSpy).toHaveBeenCalledTimes(1);
  });

  it('does not update the thread label when the user presses escape and it removes the text input', async () => {
    const newLabelText = 'new label';
    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText, '{escape}');

    expect(screen.queryByTestId('edit-thread-input')).not.toBeInTheDocument();
    expect(
      within(threadsSection).getByRole('button', { name: fakeThreads[0].metadata.label })
    ).toBeInTheDocument();
  });

  it('disables the input when enter is pressed', async () => {
    const newLabelText = 'new label';
    mockEditThreadLabel();

    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    // Not using the helper function b/c we need to reference the editInput before it is removed from the dom
    await openThreadEditDeleteMenu(fakeThreads[0].metadata.label);
    await clickEditThreadBtn();
    const editInput = screen.getByTestId('edit-thread-input');
    await userEvent.clear(editInput);
    await userEvent.type(editInput, newLabelText);
    await userEvent.keyboard('{enter}');
    expect(editInput).toBeDisabled();
  });

  it('removes the edit input when the focus on the input is lost', async () => {
    mockEditThreadLabel();
    const newLabelText = 'new label';

    threadsStore.set({
      threads: fakeThreads,
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText, '{tab}');
    expect(screen.queryByTestId('edit-thread-input')).not.toBeInTheDocument();
  });
  it('changes the active chat thread', async () => {
    const goToSpy = vi.spyOn(navigation, 'goto');

    const fakeThread = getFakeThread({ numMessages: 6 });

    threadsStore.set({
      threads: [fakeThread],
      sendingBlocked: false,
      lastVisitedThreadId: fakeThreads[0].id,
      streamingMessage: null
    });

    render(Sidebar);

    expect(
      screen.queryByRole('button', { name: getMessageText(fakeThread.messages![0]) })
    ).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: fakeThread.metadata.label }));

    expect(goToSpy).toHaveBeenCalledTimes(1);
    expect(goToSpy).toHaveBeenCalledWith(`/chat/${fakeThread.id}`);
  });
  it('search finds threads by label', async () => {
    const fakeThread1 = getFakeThread({ numMessages: 2 });
    const fakeThread2 = getFakeThread({ numMessages: 2 });
    const fakeThread3 = getFakeThread({ numMessages: 2 });

    threadsStore.set({
      threads: [fakeThread1, fakeThread2, fakeThread3],
      sendingBlocked: false,
      lastVisitedThreadId: '',
      streamingMessage: null
    });

    render(Sidebar);

    screen.getByRole('button', { name: fakeThread1.metadata.label });
    screen.getByRole('button', { name: fakeThread2.metadata.label });
    screen.getByRole('button', { name: fakeThread3.metadata.label });

    const searchBox = screen.getByPlaceholderText('Search...');
    await userEvent.type(searchBox, fakeThread2.metadata.label);

    expect(
      screen.queryByRole('button', { name: fakeThread1.metadata.label })
    ).not.toBeInTheDocument();

    expect(screen.queryByRole('button', { name: fakeThread2.metadata.label })).toBeInTheDocument();

    expect(
      screen.queryByRole('button', { name: fakeThread3.metadata.label })
    ).not.toBeInTheDocument();
  });

  it('search finds threads by messages', async () => {
    const fakeThread1 = getFakeThread({ numMessages: 2 });
    const fakeThread2 = getFakeThread({ numMessages: 2 });
    const fakeThread3 = getFakeThread({ numMessages: 2 });

    threadsStore.set({
      threads: [fakeThread1, fakeThread2, fakeThread3],
      sendingBlocked: false,
      lastVisitedThreadId: '',
      streamingMessage: null
    });

    render(Sidebar);

    screen.getByRole('button', { name: fakeThread1.metadata.label });
    screen.getByRole('button', { name: fakeThread2.metadata.label });
    screen.getByRole('button', { name: fakeThread3.metadata.label });

    const searchBox = screen.getByPlaceholderText('Search...');

    await userEvent.type(searchBox, getMessageText(fakeThread1.messages![0]));

    expect(screen.queryByRole('button', { name: fakeThread1.metadata.label })).toBeInTheDocument();

    expect(
      screen.queryByRole('button', { name: fakeThread2.metadata.label })
    ).not.toBeInTheDocument();

    expect(
      screen.queryByRole('button', { name: fakeThread3.metadata.label })
    ).not.toBeInTheDocument();
  });
});
