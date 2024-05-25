import { ChatSidebar } from '$components';
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
import stores from '$app/stores';
import { getUnixSeconds, monthNames } from '$helpers/dates';
import * as navigation from '$app/navigation';
import { getMessageText } from '$helpers/threads';

const { getStores } = await vi.hoisted(() => import('../../lib/mocks/svelte'));

const editThreadsLabel = async (oldLabel: string, newLabel: string, keyToPress = '{enter}') => {
  const overflowMenu = within(screen.getByTestId(`side-nav-menu-item-${oldLabel}`)).getByRole(
    'button',
    { name: /menu/i }
  );
  await userEvent.click(overflowMenu);
  const editBtn = within(overflowMenu).getByRole('menuitem', { name: /edit/i });
  await userEvent.click(editBtn);

  const editInput = await screen.findByLabelText('edit thread');
  await userEvent.clear(editInput);
  await userEvent.type(editInput, newLabel);
  await userEvent.keyboard(keyToPress);
};

vi.mock('$app/stores', (): typeof stores => {
  const page: typeof stores.page = {
    subscribe(fn) {
      return getStores({
        url: `http://localhost/chat/${fakeThreads[0].id}`,
        params: { thread_id: fakeThreads[0].id }
      }).page.subscribe(fn);
    }
  };
  const navigating: typeof stores.navigating = {
    subscribe(fn) {
      return getStores().navigating.subscribe(fn);
    }
  };
  const updated: typeof stores.updated = {
    subscribe(fn) {
      return getStores().updated.subscribe(fn);
    },
    check: () => Promise.resolve(false)
  };

  return {
    getStores,
    navigating,
    page,
    updated
  };
});

describe('ChatSidebar', () => {
  it('renders threads', async () => {
    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    const threadsSection = screen.getByTestId('threads');

    fakeThreads.forEach((thread) => {
      expect(within(threadsSection).getByText(thread.metadata.label)).toBeInTheDocument();
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
      threads: [fakeTodayThread, fakeYesterdayThread] // uses date override starting in March
    });

    render(ChatSidebar);
    const threadsSection = screen.getByTestId('threads');

    expect(within(threadsSection).getByText(fakeTodayThread.metadata.label)).toBeInTheDocument();
    expect(
      within(threadsSection).getByText(fakeYesterdayThread.metadata.label)
    ).toBeInTheDocument();

    expect(screen.getByText('Today')).toBeInTheDocument();
    expect(screen.getByText('Yesterday')).toBeInTheDocument();

    expect(screen.queryByText(monthNames[today.getMonth()])).not.toBeInTheDocument();
    expect(screen.queryByText(monthNames[today.getMonth() - 1])).not.toBeInTheDocument();
  });

  it('deletes threads', async () => {
    mockDeleteThread();

    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();
    expect(within(threadsSection).getByText(fakeThreads[1].metadata.label)).toBeInTheDocument();

    const overflowMenu = screen.getAllByLabelText('menu')[0];
    await userEvent.click(overflowMenu);

    const deleteBtn = within(overflowMenu).getByText('Delete');
    await userEvent.click(deleteBtn);

    const modal = screen.getByRole('presentation');

    expect(modal).toBeVisible();

    const confirmDeleteBtn = within(modal).getByText('Delete');
    await userEvent.click(confirmDeleteBtn);
    expect(modal).not.toBeVisible;

    expect(
      within(threadsSection).queryByText(fakeThreads[0].metadata.label)
    ).not.toBeInTheDocument();
    expect(within(threadsSection).getByText(fakeThreads[1].metadata.label)).toBeInTheDocument();
  });
  it('dispatches a toast when there is an error deleting a thread and it does not delete the thread from the screen', async () => {
    mockDeleteThreadError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');

    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();

    const overflowMenu = screen.getAllByLabelText('menu')[0];
    await userEvent.click(overflowMenu);

    const deleteBtn = within(overflowMenu).getByText('Delete');
    await userEvent.click(deleteBtn);

    const modal = screen.getByRole('presentation');

    expect(modal).toBeInTheDocument();

    const confirmDeleteBtn = within(modal).getByText('Delete');
    await userEvent.click(confirmDeleteBtn);

    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();
    expect(toastSpy).toHaveBeenCalledTimes(1);
  });

  it('edits thread labels', async () => {
    const newLabelText = 'new label';
    mockEditThreadLabel();

    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText);
    expect(within(threadsSection).getByText(newLabelText)).toBeInTheDocument();
  });

  it('edits thread labels when tab is pressed instead of enter', async () => {
    const newLabelText = 'new label';
    mockEditThreadLabel();

    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText, '{Tab}');
    expect(within(threadsSection).getByText(newLabelText)).toBeInTheDocument();
  });

  it('edits thread labels when the user clicks away from the input (onBlur)', async () => {
    const newLabelText = 'new label';
    mockEditThreadLabel();

    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();

    const overflowMenu = within(
      screen.getByTestId(`side-nav-menu-item-${fakeThreads[0].metadata.label}`)
    ).getByRole('button', { name: /menu/i });
    await userEvent.click(overflowMenu);
    const editBtn = within(overflowMenu).getByRole('menuitem', { name: /edit/i });
    await userEvent.click(editBtn);
    const editInput = screen.getByLabelText('edit thread');
    await userEvent.clear(editInput);
    await userEvent.type(editInput, newLabelText);

    await fireEvent.blur(editInput);
    await within(threadsSection).findByText(newLabelText);
  });

  it('dispatches a toast when there is an error editing a threads label and it does not update the label on the screen', async () => {
    mockEditThreadLabelError();
    const toastSpy = vi.spyOn(toastStore, 'addToast');

    const newLabelText = 'new label';
    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText);
    await userEvent.keyboard('{enter}');
    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();
    expect(toastSpy).toHaveBeenCalledTimes(1);
  });

  it('does not update the thread label when the user presses escape and it removes the text input', async () => {
    const newLabelText = 'new label';
    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    const threadsSection = screen.getByTestId('threads');

    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText, '{escape}');

    expect(screen.queryByLabelText('edit thread')).not.toBeInTheDocument();
    expect(within(threadsSection).getByText(fakeThreads[0].metadata.label)).toBeInTheDocument();
  });

  it('disables the input when enter is pressed', async () => {
    const newLabelText = 'new label';
    mockEditThreadLabel();

    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    // Not using the helper function b/c we need to reference the editInput at the end
    const overflowMenu = screen.getAllByLabelText('menu')[0];
    await userEvent.click(overflowMenu);
    const editBtn = within(overflowMenu).getByText('Edit');
    await userEvent.click(editBtn);
    const editInput = screen.getByLabelText('edit thread');
    await userEvent.clear(editInput);
    await userEvent.type(editInput, newLabelText);
    await userEvent.keyboard('{enter}');
    expect(editInput).toHaveProperty('readOnly', true);
  });

  it('removes the edit input when the focus on the input is lost', async () => {
    mockEditThreadLabel();
    const newLabelText = 'new label';

    threadsStore.set({
      threads: fakeThreads
    });

    render(ChatSidebar);

    await editThreadsLabel(fakeThreads[0].metadata.label, newLabelText, '{tab}');
    const editInput = screen.queryByText('edit thread');
    expect(editInput).not.toBeInTheDocument();
  });
  it('changes the active chat thread', async () => {
    const goToSpy = vi.spyOn(navigation, 'goto');

    const fakeThread = getFakeThread({ numMessages: 6 });

    threadsStore.set({
      threads: [fakeThread]
    });

    render(ChatSidebar);

    expect(screen.queryByText(getMessageText(fakeThread.messages![0]))).not.toBeInTheDocument();

    await userEvent.click(screen.getByText(fakeThread.metadata.label));

    expect(goToSpy).toHaveBeenCalledTimes(1);
    expect(goToSpy).toHaveBeenCalledWith(`/chat/${fakeThread.id}`);
  });
  it('search finds threads by label', async () => {
    const fakeThread1 = getFakeThread({ numMessages: 2 });
    const fakeThread2 = getFakeThread({ numMessages: 2 });
    const fakeThread3 = getFakeThread({ numMessages: 2 });

    threadsStore.set({
      threads: [fakeThread1, fakeThread2, fakeThread3]
    });

    render(ChatSidebar);

    expect(screen.queryByText(fakeThread1.metadata.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeThread2.metadata.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeThread3.metadata.label)).toBeInTheDocument();

    const searchBox = screen.getByPlaceholderText('Search...');
    await userEvent.type(searchBox, fakeThread2.metadata.label);

    expect(screen.queryByText(fakeThread1.metadata.label)).not.toBeInTheDocument();
    expect(screen.queryByText(fakeThread2.metadata.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeThread3.metadata.label)).not.toBeInTheDocument();
  });

  it('search finds threads by messages', async () => {
    const fakeThread1 = getFakeThread({ numMessages: 2 });
    const fakeThread2 = getFakeThread({ numMessages: 2 });
    const fakeThread3 = getFakeThread({ numMessages: 2 });

    threadsStore.set({
      threads: [fakeThread1, fakeThread2, fakeThread3]
    });

    render(ChatSidebar);

    expect(screen.queryByText(fakeThread1.metadata.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeThread2.metadata.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeThread3.metadata.label)).toBeInTheDocument();

    const searchBox = screen.getByPlaceholderText('Search...');

    await userEvent.type(searchBox, getMessageText(fakeThread1.messages![0]));

    expect(screen.queryByText(fakeThread1.metadata.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeThread2.metadata.label)).not.toBeInTheDocument();
    expect(screen.queryByText(fakeThread3.metadata.label)).not.toBeInTheDocument();
  });
});
