<script lang="ts">
  import {
    ASSISTANTS_DESCRIPTION_MAX_LENGTH,
    ASSISTANTS_INSTRUCTIONS_MAX_LENGTH,
    ASSISTANTS_NAME_MAX_LENGTH
  } from '$lib/constants';
  import { superForm } from 'sveltekit-superforms';
  import { page } from '$app/stores';
  import { beforeNavigate, goto } from '$app/navigation';
  import { Button, Modal, P } from 'flowbite-svelte';
  import Slider from '$components/Slider.svelte';
  import { yup } from 'sveltekit-superforms/adapters';
  import { assistantsStore, filesStore, toastStore, uiStore } from '$stores';
  import { assistantInputSchema, editAssistantInputSchema } from '$lib/schemas/assistants';
  import type { NavigationTarget } from '@sveltejs/kit';
  import { onMount } from 'svelte';
  import AssistantFileSelect from '$components/AssistantFileSelect.svelte';
  import LFInput from '$components/LFInput.svelte';
  import LFLabel from '$components/LFLabel.svelte';
  import AssistantAvatar from '$components/AssistantAvatar.svelte';
  import vectorStatusStore from '$stores/vectorStatusStore.js';

  export let data;
  export let isEditMode = $page.url.pathname.includes('edit');

  let bypassCancelWarning = false;

  $: assistant = $assistantsStore.assistants.find(
    (assistant) => assistant.id === $page.params.assistantId
  );

  const { form, errors, enhance, submitting, isTainted, delayed } = superForm(data.form, {
    invalidateAll: false,
    validators: yup(isEditMode ? editAssistantInputSchema : assistantInputSchema),
    onResult: async ({ result }) => {
      if (result.type === 'success') {
        const vectorStoreId = result.data.assistant?.tool_resources?.file_search
          ?.vector_store_ids?.[0] as string;

        if (!uiStore.isUsingOpenAI && vectorStoreId) {
          toastStore.addToast({
            kind: 'info',
            title: `Updating Assistant Files`,
            subtitle: result.data.assistant.name,
            fileIds: result.data.fileIds,
            vectorStoreId: vectorStoreId,
            variant: 'assistant-progress',
            timeout: -1 // no expiration
          });
          // If the assistant is being edited and previously had files with "completed" vector status,
          // we need to fetch those statuses. The realtime listener will not detect a change for those old files and
          // will not update the vectorStatusStore.
          await vectorStatusStore.updateAllStatusesForVector(vectorStoreId);
        } else {
          toastStore.addToast({
            kind: 'success',
            title: `Assistant ${isEditMode ? 'Updated' : 'Created'}.`
          });
        }

        bypassCancelWarning = true;
        if (isEditMode) {
          assistantsStore.updateAssistant(result.data.assistant);
        } else {
          assistantsStore.addAssistant(result.data.assistant);
        }
        await goto(result.data.redirectUrl);
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
        title: 'Error importing assistant'
      });
      goto('/chat/assistants-management');
    }
    filesStore.setSelectedAssistantFileIds($form.data_sources || []);
  });
</script>

<form method="POST" enctype="multipart/form-data" use:enhance class="w-1/2">
  <div class="flex flex-col py-2">
    <div class="flex items-center justify-between">
      <h5 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">
        {`${isEditMode ? 'Edit' : 'New'} Assistant`}
      </h5>

      <AssistantAvatar {form} />
    </div>
    <input type="hidden" name="id" value={$form.id} />
    <LFInput
      id="name"
      name="name"
      label="Name *"
      placeholder="Assistant name"
      autocomplete="off"
      bind:value={$form.name}
      maxlength={ASSISTANTS_NAME_MAX_LENGTH}
      errorText={!!$errors.name && $errors.name.toString()}
    />

    <LFInput
      id="description"
      name="description"
      label="Tagline *"
      placeholder="Here to help..."
      autocomplete="off"
      bind:value={$form.description}
      maxlength={ASSISTANTS_DESCRIPTION_MAX_LENGTH}
      tooltipText="Taglines display on assistant tiles"
      errorText={!!$errors.description && $errors.description.toString()}
    />

    <LFInput
      id="instructions"
      name="instructions"
      label="Instructions *"
      placeholder="You'll act as..."
      autocomplete="off"
      textArea
      bind:value={$form.instructions}
      maxlength={ASSISTANTS_INSTRUCTIONS_MAX_LENGTH}
      tooltipText="Detailed instructions to guide your assistant's responses and behavior"
      errorText={!!$errors.instructions && $errors.instructions.toString()}
    />

    <Slider
      id="temperature"
      label="Temperature"
      bind:value={$form.temperature}
      tooltipText="Adjust the slider to set the creativity level of your assistant's responses"
      showThumb={false}
    />
    <input type="hidden" name="temperature" value={$form.temperature} />

    <div class="mb-6">
      <LFLabel
        id="data_sources"
        tooltipText="Specific files your assistant can search and reference">Data Sources</LFLabel
      >
      <AssistantFileSelect filesForm={data.filesForm} />
    </div>

    <input
      type="hidden"
      name="vectorStoreId"
      value={assistant?.tool_resources?.file_search?.vector_store_ids[0] || undefined}
    />

    <div>
      <Button
        data-testid="assistant-form-cancel-btn"
        color="alternative"
        on:click={() => {
          bypassCancelWarning = true;
          goto('/chat/assistants-management');
        }}>Cancel</Button
      >

      <Button type="submit" disabled={$submitting || $filesStore.uploading}>Save</Button>
      {#if $delayed}
        <P class="inline text-gray-700 dark:text-gray-400">Processing, please wait...</P>
      {/if}
    </div>
  </div>
</form>

<Modal bind:open={cancelModalOpen} title="Unsaved Changes" color="primary"
  ><P class="dark:text-gray-400"
    >You have unsaved changes. Do you want to leave this page? Unsaved changes will be deleted.</P
  >
  <div class="flex justify-end gap-2">
    <Button color="alternative" on:click={() => (cancelModalOpen = false)} size="sm"
      >Stay on page</Button
    >
    <Button
      color="red"
      on:click={() => {
        leavePageConfirmed = true;
        if (navigateTo) goto(navigateTo.url.href);
      }}
      size="sm">Leave this page</Button
    >

    <div class="flex justify-end gap-2"></div>
  </div></Modal
>
