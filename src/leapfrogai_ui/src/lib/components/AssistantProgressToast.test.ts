/*
Note - fully testing the assistant progress toast has proven difficult with Playwright. Sometimes the websocket
 connection for the Supabase realtime listeners works, and sometimes it does not. Due to the dynamic nature of
 how this component updates in realtime, unit testing is limited.
 There is an issue in the backlog to re-address at some point:
 TODO - https://github.com/defenseunicorns/leapfrogai/issues/981
*/

import AssistantProgressToast from '$components/AssistantProgressToast.svelte';
import { render, screen } from '@testing-library/svelte';
import filesStore from '$stores/filesStore';
import { getFakeFiles } from '$testUtils/fakeData';
import { convertFileObjectToLFFileObject } from '$helpers/fileHelpers';
import { delay } from 'msw';
import { vi } from 'vitest';
import { toastStore } from '$stores';

describe('AssistantProgressToast', () => {
  it('is auto dismissed after a specified timeout', async () => {
    const dismissToastSpy = vi.spyOn(toastStore, 'dismissToast');
    const files = getFakeFiles({ numFiles: 2 });
    const toastId = '1';
    const toast: ToastNotificationProps = {
      id: toastId,
      kind: 'info',
      title: '',
      fileIds: files.map((file) => file.id),
      vectorStoreId: '123'
    };
    filesStore.setFiles(convertFileObjectToLFFileObject(files));

    const timeout = 10; //10ms
    render(AssistantProgressToast, { timeout, toast }); //10ms timeout
    await screen.findByText('Updating Assistant Files');
    await delay(timeout + 1);
    expect(dismissToastSpy).toHaveBeenCalledWith(toastId);
  });
});
