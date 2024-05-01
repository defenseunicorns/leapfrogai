import { ChatSidebar } from '$components';
import {
  mockDeleteConversation,
  mockDeleteConversationError,
  mockEditConversationLabel,
  mockEditConversationLabelError
} from '$lib/mocks/chat-mocks';
import { conversationsStore, toastStore } from '$stores';
import { fireEvent, render, screen, within } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { fakeConversations, getFakeConversation } from '../../testUtils/fakeData';
import { vi } from 'vitest';
import stores from '$app/stores';
import { monthNames } from '$helpers/dates';
import * as navigation from '$app/navigation';

const { getStores } = await vi.hoisted(() => import('../../lib/mocks/svelte'));

const editConversationLabel = async (
  oldLabel: string,
  newLabel: string,
  keyToPress = '{enter}'
) => {
  const overflowMenu = within(screen.getByTestId(`side-nav-menu-item-${oldLabel}`)).getByRole(
    'button',
    { name: /menu/i }
  );
  await userEvent.click(overflowMenu);
  const editBtn = within(overflowMenu).getByRole('menuitem', { name: /edit/i });
  await userEvent.click(editBtn);

  const editInput = await screen.findByLabelText('edit conversation');
  await userEvent.clear(editInput);
  await userEvent.type(editInput, newLabel);
  await userEvent.keyboard(keyToPress);
};

vi.mock('$app/stores', (): typeof stores => {
  const page: typeof stores.page = {
    subscribe(fn) {
      return getStores({
        url: `http://localhost/chat/${fakeConversations[0].id}`,
        params: { conversation_id: fakeConversations[0].id }
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
  it('renders conversations', async () => {
    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    const conversationsSection = screen.getByTestId('conversations');

    fakeConversations.forEach((conversation) => {
      expect(within(conversationsSection).getByText(conversation.label)).toBeInTheDocument();
    });
  });

  it('does not render date categories that have no conversations', async () => {
    const today = new Date();
    const fakeTodayConversation = getFakeConversation();
    const fakeYesterdayConversation = getFakeConversation({
      insertedAt: new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate() - 1
      ).toDateString()
    });

    conversationsStore.set({
      conversations: [fakeTodayConversation, fakeYesterdayConversation] // uses date override starting in March
    });

    render(ChatSidebar);
    const conversationsSection = screen.getByTestId('conversations');

    expect(within(conversationsSection).getByText(fakeTodayConversation.label)).toBeInTheDocument();
    expect(
      within(conversationsSection).getByText(fakeYesterdayConversation.label)
    ).toBeInTheDocument();

    expect(screen.getByText('Today')).toBeInTheDocument();
    expect(screen.getByText('Yesterday')).toBeInTheDocument();

    expect(screen.queryByText(monthNames[today.getMonth()])).not.toBeInTheDocument();
    expect(screen.queryByText(monthNames[today.getMonth() - 1])).not.toBeInTheDocument();
  });

  it('deletes conversations', async () => {
    mockDeleteConversation();

    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    const conversationsSection = screen.getByTestId('conversations');

    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();
    expect(within(conversationsSection).getByText(fakeConversations[1].label)).toBeInTheDocument();

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
      within(conversationsSection).queryByText(fakeConversations[0].label)
    ).not.toBeInTheDocument();
    expect(within(conversationsSection).getByText(fakeConversations[1].label)).toBeInTheDocument();
  });
  it('dispatches a toast when there is an error deleting a conversation and it does not delete the conversation from the screen', async () => {
    mockDeleteConversationError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');

    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    const conversationsSection = screen.getByTestId('conversations');

    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();

    const overflowMenu = screen.getAllByLabelText('menu')[0];
    await userEvent.click(overflowMenu);

    const deleteBtn = within(overflowMenu).getByText('Delete');
    await userEvent.click(deleteBtn);

    const modal = screen.getByRole('presentation');

    expect(modal).toBeInTheDocument();

    const confirmDeleteBtn = within(modal).getByText('Delete');
    await userEvent.click(confirmDeleteBtn);

    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();
    expect(toastSpy).toHaveBeenCalledTimes(1);
  });

  it('edits conversation labels', async () => {
    const newLabelText = 'new label';
    mockEditConversationLabel();

    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    const conversationsSection = screen.getByTestId('conversations');

    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();

    await editConversationLabel(fakeConversations[0].label, newLabelText);
    expect(within(conversationsSection).getByText(newLabelText)).toBeInTheDocument();
  });

  it('edits conversation labels when tab is pressed instead of enter', async () => {
    const newLabelText = 'new label';
    mockEditConversationLabel();

    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    const conversationsSection = screen.getByTestId('conversations');

    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();

    await editConversationLabel(fakeConversations[0].label, newLabelText, '{Tab}');
    expect(within(conversationsSection).getByText(newLabelText)).toBeInTheDocument();
  });

  it('edits conversation labels when the user clicks away from the input (onBlur)', async () => {
    const newLabelText = 'new label';
    mockEditConversationLabel();

    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    const conversationsSection = screen.getByTestId('conversations');

    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();

    const overflowMenu = within(
      screen.getByTestId(`side-nav-menu-item-${fakeConversations[0].label}`)
    ).getByRole('button', { name: /menu/i });
    await userEvent.click(overflowMenu);
    const editBtn = within(overflowMenu).getByRole('menuitem', { name: /edit/i });
    await userEvent.click(editBtn);
    const editInput = screen.getByLabelText('edit conversation');
    await userEvent.clear(editInput);
    await userEvent.type(editInput, newLabelText);

    await fireEvent.blur(editInput);
    await within(conversationsSection).findByText(newLabelText);
  });

  it('dispatches a toast when there is an error editing a conversations label and it does not update the label on the screen', async () => {
    mockEditConversationLabelError();
    const toastSpy = vi.spyOn(toastStore, 'addToast');

    const newLabelText = 'new label';
    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    const conversationsSection = screen.getByTestId('conversations');

    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();

    await editConversationLabel(fakeConversations[0].label, newLabelText);
    await userEvent.keyboard('{enter}');
    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();
    expect(toastSpy).toHaveBeenCalledTimes(1);
  });

  it('does not update the conversation label when the user presses escape and it removes the text input', async () => {
    const newLabelText = 'new label';
    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    const conversationsSection = screen.getByTestId('conversations');

    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();

    await editConversationLabel(fakeConversations[0].label, newLabelText, '{escape}');

    expect(screen.queryByLabelText('edit conversation')).not.toBeInTheDocument();
    expect(within(conversationsSection).getByText(fakeConversations[0].label)).toBeInTheDocument();
  });

  it('disables the input when enter is pressed', async () => {
    const newLabelText = 'new label';
    mockEditConversationLabel();

    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    // Not using the helper function b/c we need to reference the editInput at the end
    const overflowMenu = screen.getAllByLabelText('menu')[0];
    await userEvent.click(overflowMenu);
    const editBtn = within(overflowMenu).getByText('Edit');
    await userEvent.click(editBtn);
    const editInput = screen.getByLabelText('edit conversation');
    await userEvent.clear(editInput);
    await userEvent.type(editInput, newLabelText);
    await userEvent.keyboard('{enter}');
    expect(editInput).toHaveProperty('readOnly', true);
  });

  it('removes the edit input when the focus on the input is lost', async () => {
    mockEditConversationLabel();
    const newLabelText = 'new label';

    conversationsStore.set({
      conversations: fakeConversations
    });

    render(ChatSidebar, { isSideNavOpen: true });

    await editConversationLabel(fakeConversations[0].label, newLabelText, '{tab}');
    const editInput = screen.queryByText('edit conversation');
    expect(editInput).not.toBeInTheDocument();
  });
  it('changes the active chat thread', async () => {
    const goToSpy = vi.spyOn(navigation, 'goto');

    const fakeConversation = getFakeConversation({ numMessages: 6 });

    conversationsStore.set({
      conversations: [fakeConversation]
    });

    render(ChatSidebar, { isSideNavOpen: true });

    expect(screen.queryByText(fakeConversation.messages[0].content)).not.toBeInTheDocument();

    await userEvent.click(screen.getByText(fakeConversation.label));

    expect(goToSpy).toHaveBeenCalledTimes(1);
    expect(goToSpy).toHaveBeenCalledWith(`/chat/${fakeConversation.id}`);
  });
  it('search finds conversations by label', async () => {
    const fakeConversation1 = getFakeConversation({ numMessages: 2 });
    const fakeConversation2 = getFakeConversation({ numMessages: 2 });
    const fakeConversation3 = getFakeConversation({ numMessages: 2 });

    conversationsStore.set({
      conversations: [fakeConversation1, fakeConversation2, fakeConversation3]
    });

    render(ChatSidebar, { isSideNavOpen: true });

    expect(screen.queryByText(fakeConversation1.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeConversation2.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeConversation3.label)).toBeInTheDocument();

    const searchBox = screen.getByPlaceholderText('Search...');
    await userEvent.type(searchBox, fakeConversation2.label);

    expect(screen.queryByText(fakeConversation1.label)).not.toBeInTheDocument();
    expect(screen.queryByText(fakeConversation2.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeConversation3.label)).not.toBeInTheDocument();
  });

  it('search finds conversations by messages', async () => {
    const fakeConversation1 = getFakeConversation({ numMessages: 2 });
    const fakeConversation2 = getFakeConversation({ numMessages: 2 });
    const fakeConversation3 = getFakeConversation({ numMessages: 2 });

    conversationsStore.set({
      conversations: [fakeConversation1, fakeConversation2, fakeConversation3]
    });

    render(ChatSidebar, { isSideNavOpen: true });

    expect(screen.queryByText(fakeConversation1.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeConversation2.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeConversation3.label)).toBeInTheDocument();

    const searchBox = screen.getByPlaceholderText('Search...');
    await userEvent.type(searchBox, fakeConversation1.messages[0].content);

    expect(screen.queryByText(fakeConversation1.label)).toBeInTheDocument();
    expect(screen.queryByText(fakeConversation2.label)).not.toBeInTheDocument();
    expect(screen.queryByText(fakeConversation3.label)).not.toBeInTheDocument();
  });
});
