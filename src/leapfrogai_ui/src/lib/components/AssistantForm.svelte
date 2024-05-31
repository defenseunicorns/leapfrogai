<script lang="ts">
  import {
    ASSISTANTS_DESCRIPTION_MAX_LENGTH,
    ASSISTANTS_INSTRUCTIONS_MAX_LENGTH,
    ASSISTANTS_NAME_MAX_LENGTH
  } from '$lib/constants';
  import { superForm } from 'sveltekit-superforms';
  import { Add } from 'carbon-icons-svelte';
  import { page } from '$app/stores';
  import { beforeNavigate, goto, invalidate } from '$app/navigation';
  import { Button, Modal, Slider, TextArea, TextInput } from 'carbon-components-svelte';
  import AssistantAvatar from '$components/AssistantAvatar.svelte';
  import { yup } from 'sveltekit-superforms/adapters';
  import { toastStore } from '$stores';
  import InputTooltip from '$components/InputTooltip.svelte';
  import { editAssistantInputSchema, assistantInputSchema } from '$lib/schemas/assistants';
  import type { NavigationTarget } from '@sveltejs/kit';
  import { onMount } from 'svelte';

  export let data;

  let isEditMode = $page.url.pathname.includes('edit');
  let bypassCancelWarning = false;

  const { form, errors, enhance, submitting, isTainted } = superForm(data.form, {
    invalidateAll: false,
    validators: yup(isEditMode ? editAssistantInputSchema : assistantInputSchema),
    onResult({ result }) {
      invalidate('/api/assistants');
      if (result.type === 'redirect') {
        toastStore.addToast({
          kind: 'success',
          title: `Assistant ${isEditMode ? 'Updated' : 'Created'}.`,
          subtitle: ''
        });
        bypassCancelWarning = true;
        goto(result.location);
      } else if (result.type === 'failure') {
        // 400 errors will show errors for the respective fields, do not show toast
        if (result.status !== 400) {
          toastStore.addToast({
            kind: 'error',
            title: `Error ${isEditMode ? 'Editing' : 'Creating'} Assistant`,
            subtitle: result.data?.message || 'An unknown error occurred.'
          });
        }
      } else if (result.type === 'error') {
        toastStore.addToast({
          kind: 'error',
          title: `Error ${isEditMode ? 'Editing' : 'Creating'} Assistant`,
          subtitle: result.error?.message || 'An unknown error occurred.'
        });
      }
    }
  });

  let cancelModalOpen = false;
  let files: File[] = [];
  let selectedPictogramName = isEditMode ? $form.pictogram : 'default';

  let navigateTo: NavigationTarget;
  let leavePageConfirmed = false;

  // Show cancel modal if form is tainted and user attempts to navigate away
  beforeNavigate(({ cancel, to, type }) => {
    if (to) {
      navigateTo = to;
    }
    if (!leavePageConfirmed && isTainted() && !bypassCancelWarning) {
      cancel();
      leavePageConfirmed = false; // reset
      if (type !== 'leave') {
        // if leaving app, don't show cancel modal (ex. refresh page), triggers the native browser unload confirmation dialog.
        cancelModalOpen = true;
      }
    }
  });

  onMount(() => {
    if (isEditMode && Object.keys($errors).length > 0) {
      toastStore.addToast({
        kind: 'error',
        title: 'Error importing assistant',
        subtitle: ''
      });
      goto('/chat/assistants-management');
    }
  });
</script>

<form method="POST" enctype="multipart/form-data" use:enhance class="assistant-form">
  <div class="container">
    <div class="inner-container">
      <div class="top-row">
        <div class="title">{`${isEditMode ? 'Edit' : 'New'} Assistant`}</div>
        <AssistantAvatar bind:files bind:selectedPictogramName {form} />
      </div>
      <input type="hidden" name="id" value={$form.id} />
      <TextInput
        name="name"
        autocomplete="off"
        labelText="Name"
        placeholder="Assistant name"
        bind:value={$form.name}
        maxlength={ASSISTANTS_NAME_MAX_LENGTH}
        invalid={!!$errors.name}
        invalidText={$errors.name?.toString()}
      />

      <InputTooltip
        name="description"
        labelText="Tagline"
        tooltipText="Taglines display on assistant tiles"
      />

      <TextInput
        name="description"
        autocomplete="off"
        placeholder="Here to help..."
        labelText="Description"
        hideLabel
        bind:value={$form.description}
        maxlength={ASSISTANTS_DESCRIPTION_MAX_LENGTH}
        invalid={!!$errors.description}
        invalidText={$errors.description?.toString()}
      />

      <InputTooltip
        name="instructions"
        labelText="Instructions"
        tooltipText="Detailed instructions to guide your assistant's responses and behavior"
      />

      <TextArea
        name="instructions"
        autocomplete="off"
        labelText="Instructions"
        bind:value={$form.instructions}
        rows={6}
        placeholder="You'll act as..."
        hideLabel
        invalid={!!$errors.instructions}
        invalidText={$errors.instructions?.toString()}
        maxlength={ASSISTANTS_INSTRUCTIONS_MAX_LENGTH}
      />

      <InputTooltip
        name="temperature"
        labelText="Temperature"
        tooltipText="Adjust the slider to set the creativity level of your assistant's responses"
      />
      <Slider
        name="temperature"
        bind:value={$form.temperature}
        hideLabel
        hideTextInput
        fullWidth
        min={0}
        max={1}
        step={0.1}
        minLabel="Min"
        maxLabel="Max"
        invalid={!!$errors.temperature}
      />

      <!--Note - Data Sources is a placeholder and will be completed in a future story-->
      <InputTooltip
        name="data_sources"
        labelText="Data Sources"
        tooltipText="Specific files your assistant can search and reference"
      />
      <div>
        <Button icon={Add} kind="secondary" size="small"
          >Add <input name="data_sources" type="hidden" /></Button
        >
      </div>

      <div>
        <Button
          kind="secondary"
          size="small"
          on:click={() => {
            bypassCancelWarning = true;
            goto('/chat/assistants-management');
          }}>Cancel</Button
        >
        <Button kind="primary" size="small" type="submit" disabled={$submitting}>Save</Button>
      </div>
    </div>
  </div>
</form>

<div class="cancel-modal">
  <Modal
    bind:open={cancelModalOpen}
    modalHeading="Unsaved Changes"
    primaryButtonText="Leave this page"
    secondaryButtonText="Stay on page"
    on:click:button--secondary={() => (cancelModalOpen = false)}
    on:submit={() => {
      leavePageConfirmed = true;
      if (navigateTo) goto(navigateTo.url.href);
    }}
    ><p>
      You have unsaved changes. Do you want to leave this page? Unsaved changes will be deleted.
    </p></Modal
  >
</div>

<style lang="scss">
  .assistant-form {
    .container {
      display: flex;
      justify-content: center;
    }
    .inner-container {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      width: 50%;
      padding-top: 0.5rem;
      padding-bottom: 0.5rem;
    }
    .top-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .title {
      @include type.type-style('heading-05');
    }

    .cancel-modal {
      :global(.bx--modal-container) {
        position: absolute;
        top: 25%;
      }
    }
  }
</style>
