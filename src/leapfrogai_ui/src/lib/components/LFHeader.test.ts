import { render, screen } from '@testing-library/svelte';
import { LFHeader } from '$components/index';
import userEvent from '@testing-library/user-event';
import { threadsStore } from '$stores';
import { getFakeThread } from '$testUtils/fakeData';

describe('LFHeader', () => {
  it('has a link on the logo that navigates to the last visited thread id', async () => {
    const thread = getFakeThread();
    threadsStore.set({
      threads: [thread],
      lastVisitedThreadId: thread.id,
      sendingBlocked: false,
      streamingMessage: null
    });

    render(LFHeader);
    expect(screen.getByTestId('logo-link')).toHaveAttribute('href', `/chat/${thread.id}`);
  });
  it('has a settings btn dropdown with links to various pages', async () => {
    render(LFHeader);
    await userEvent.click(screen.getByTestId('header-settings-btn'));

    expect(screen.getByRole('link', { name: /assistants management/i })).toHaveAttribute(
      'href',
      '/chat/assistants-management'
    );

    expect(screen.getByRole('link', { name: /file management/i })).toHaveAttribute(
      'href',
      '/chat/file-management'
    );

    expect(screen.getByRole('link', { name: /api keys/i })).toHaveAttribute(
      'href',
      '/chat/api-keys'
    );
  });

  it('has a profile btn dropdown with a logout btn', async () => {
    render(LFHeader);
    await userEvent.click(screen.getByTestId('header-profile-btn'));

    screen.getByRole('button', {
      name: /log out/i
    });
  });
});
