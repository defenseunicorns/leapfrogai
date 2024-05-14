<script lang="ts">
  import {
    ASSISTANTS_DESCRIPTION_MAX_LENGTH,
    ASSISTANTS_INSTRUCTIONS_MAX_LENGTH,
    ASSISTANTS_NAME_MAX_LENGTH
  } from '$lib/constants';
  import { superForm } from 'sveltekit-superforms';
  import { Add } from 'carbon-icons-svelte';
  import { goto } from '$app/navigation';
  import { Button, Modal, Slider, TextArea, TextInput } from 'carbon-components-svelte';
  import AssistantAvatar from '$components/AssistantAvatar.svelte';
  import { yup } from 'sveltekit-superforms/adapters';
  import { supabaseAssistantInputSchema } from '../../../../../../schemas/assistants';
  import { toastStore } from '$stores';
  import InputTooltip from '$components/InputTooltip.svelte';
  import { env } from '$env/dynamic/public';

  export let data;

  const { form, errors, enhance, submitting } = superForm(data.form, {
    validators: yup(supabaseAssistantInputSchema),
    onResult({ result }) {
      if (result.type === 'redirect') {
        toastStore.addToast({
          kind: 'success',
          title: 'Assistant Updated.',
          subtitle: ''
        });
        goto(result.location);
      } else if (result.type === 'failure') {
        // 400 errors will show errors for the respective fields, do not show toast
        if (result.status !== 400) {
          toastStore.addToast({
            kind: 'error',
            title: 'Error Editing Assistant',
            subtitle: result.data?.message || 'An unknown error occurred.'
          });
        }
      } else if (result.type === 'error') {
        toastStore.addToast({
          kind: 'error',
          title: 'Error Editing Assistant',
          subtitle: result.error?.message || 'An unknown error occurred.'
        });
      }
    }
  });
  let cancelModalOpen = false;
  let files: File[] = [];
  let selectedPictogramName = data.assistant.metadata.pictogram || 'default';
  let avatarPath = data.assistant.metadata.avatar;

  // Get image url for Avatar if the assistant has an avatar
  $: avatarUrl = avatarPath
    ? `${env.PUBLIC_SUPABASE_URL}/storage/v1/object/public/assistant_avatars/${avatarPath}`
    : '';
</script>

<form method="POST" enctype="multipart/form-data" use:enhance class="assistant-form">
  <div class="container">
    <div class="inner-container">
      <div class="top-row">
        <div class="title">Edit Assistant</div>
        <AssistantAvatar bind:files bind:selectedPictogramName {avatarUrl} />
      </div>
      <input type="hidden" name="id" value={$form.id} />
      <TextInput
        name="name"
        labelText="Name"
        placeholder="Assistant name"
        bind:value={$form.name}
        maxlength={ASSISTANTS_NAME_MAX_LENGTH}
        invalid={!!$errors.name}
        invalidText={$errors.name}
      />

      <InputTooltip
        name="description"
        labelText="Tagline"
        tooltipText="Taglines display on assistant tiles"
      />

      <TextInput
        name="description"
        placeholder="Here to help..."
        labelText="Description"
        hideLabel
        bind:value={$form.description}
        maxlength={ASSISTANTS_DESCRIPTION_MAX_LENGTH}
        invalid={!!$errors.description}
        invalidText={$errors.description}
      />

      <InputTooltip
        name="instructions"
        labelText="Instructions"
        tooltipText="Detailed instructions to guide your assistant's responses and behavior"
      />

      <TextArea
        name="instructions"
        labelText="Instructions"
        bind:value={$form.instructions}
        rows={6}
        placeholder="You'll act as..."
        hideLabel
        invalid={!!$errors.instructions}
        invalidText={$errors.instructions}
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
        invalidText={$errors.temperature}
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
        <Button kind="secondary" size="small" on:click={() => (cancelModalOpen = true)}
          >Cancel</Button
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
    on:submit={() => goto('/chat/assistants-management')}
    ><p>
      You have unsaved changes. Do you want to leave this page? Unsaved changes will be deleted.
    </p></Modal
  >
</div>
