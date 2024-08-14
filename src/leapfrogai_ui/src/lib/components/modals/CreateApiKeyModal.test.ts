import { render, screen, within } from '@testing-library/svelte';
import CreateApiKeyModal from '$components/modals/CreateApiKeyModal.svelte';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { vi } from 'vitest';
import type { APIKeysForm } from '$lib/types/apiKeys';
import { newAPIKeySchema } from '$schemas/apiKey';
import { toastStore } from '$stores';
import { faker } from '@faker-js/faker';
import userEvent from '@testing-library/user-event';
import { mockCreateApiKeyFormActionError } from '$lib/mocks/api-key-mocks';

// TODO - this test will not work until we get a response to this question:
// https://github.com/ciscoheat/sveltekit-superforms/issues/394
// This is currently blocking this issue: https://github.com/defenseunicorns/leapfrogai/issues/636
describe.skip('Create API Key Modal', () => {
  let form: APIKeysForm;

  it('closes the modal and pops a toast when there is an error with the form action', async () => {
    const keyName = faker.word.noun();
    const sixtyDays = new Date();
    sixtyDays.setDate(sixtyDays.getDate() + 60);

    mockCreateApiKeyFormActionError();

    const toastSpy = vi.spyOn(toastStore, 'addToast');

    form = await superValidate(yup(newAPIKeySchema));
    render(CreateApiKeyModal, { createApiKeyModalOpen: true, form });

    const modal = screen.getByTestId('create-api-key-modal');
    await userEvent.type(within(modal).getByRole('textbox'), keyName);
    await userEvent.click(screen.getByText('60 Days'));
    await userEvent.click(within(modal).getByRole('button', { name: /create/i }));

    expect(toastSpy).toHaveBeenCalledWith({
      kind: 'error',
      title: 'Creation Failed'
    });
    expect(modal).not.toBeInTheDocument();
  });
});
