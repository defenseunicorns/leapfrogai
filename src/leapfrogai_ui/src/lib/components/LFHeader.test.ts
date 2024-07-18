import { render, screen } from '@testing-library/svelte';
import { LFHeader } from '$components/index';
import userEvent from '@testing-library/user-event';
import { threadsStore } from '$stores';
import { getFakeThread } from '$testUtils/fakeData';

describe('LFHeader', () => {
  it('closes the other header actions when one is opened', async () => {
    // We cannot test by visibility because carbon components svelte does not give us a way to grab the panel
    // in our test. The best we can do is check that the bx--header__action--active class is correctly
    // applied or not applied to the button that controls the panel
    render(LFHeader, { isUsingOpenAI: false });
    // both closed
    expect(screen.queryByText('settings-drawer')).not.toBeInTheDocument();
    expect(screen.queryByText('user-drawer')).not.toBeInTheDocument();

    // open settings
    await userEvent.click(screen.getByTestId('header-settings-btn'));
    screen.getByTestId('settings-drawer');
    expect(screen.queryByText('user-drawer')).not.toBeInTheDocument();

    // open user
    await userEvent.click(screen.getByTestId('header-user-btn'));
    expect(screen.queryByText('settings-drawer')).not.toBeInTheDocument();
    screen.getByTestId('user-drawer');
  });
  it('has a link on the logo that navigates to the last visited thread id', async () => {
    const thread = getFakeThread();
    threadsStore.set({
      threads: [thread],
      lastVisitedThreadId: thread.id,
      selectedAssistantId: '',
      sendingBlocked: false
    });

    render(LFHeader, { isUsingOpenAI: false });
    expect(screen.getByTestId('logo-link')).toHaveAttribute('href', `/chat/${thread.id}`);
  });
});
