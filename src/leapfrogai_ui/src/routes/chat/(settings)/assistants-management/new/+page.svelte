<script lang="ts">
  import { createForm } from 'svelte-forms-lib';
  import { enhance } from '$app/forms';
  import { Add } from 'carbon-icons-svelte';
  import { Button, Modal, Slider, TextArea, TextInput } from 'carbon-components-svelte';
  import { toastStore } from '$stores';
  import { goto } from '$app/navigation';
  import InputTooltip from '$components/InputTooltip.svelte';
  import { ASSISTANTS_INSTRUCTIONS_MAX_LENGTH, DEFAULT_ASSISTANT_TEMP } from '$lib/constants';
  import { supabaseAssistantInputSchema } from '../../../../../schemas/assistants';
  import {
    ASSISTANTS_DESCRIPTION_MAX_LENGTH,
    ASSISTANTS_NAME_MAX_LENGTH
  } from '$lib/constants/index.js';
  import AssistantAvatar from '$components/AssistantAvatar.svelte';

  let cancelModalOpen = false;
  let files: File[];
  let selectedPictogramName: string;

  const { form, errors, state, handleChange, updateField } = createForm({
    initialValues: {
      name: '',
      description: '',
      instructions: '',
      temperature: DEFAULT_ASSISTANT_TEMP,
      data_sources: '',
      avatar: null,
      pictogram: null
    },
    validationSchema: supabaseAssistantInputSchema,
    onSubmit: () => {}
  });

  // TODO - save pictorgram if not user image upload
  // TODO - error status for image upload - ask Greg, how is this required?

  const handleSliderChange = () => {
    /* We can't use svelte-forms-lib handleChange here because if the user clicks on the slider track instead
       of clicking and dragging the handle, svelte-forms-lib is adding an extra key called "undefined" to the form 
       values which prevents submission 
     */
    updateField('temperature', $form.temperature);
  };
</script>

<form
  method="POST"
  enctype="multipart/form-data"
  use:enhance={() => {

    return async ({ result }) => {
      if (result.type === 'redirect') {
        toastStore.addToast({
          kind: 'success',
          title: 'Assistant Created.',
          subtitle: ''
        });
        await goto(result.location);
      } else if (result.type === 'failure') {
        toastStore.addToast({
          kind: 'error',
          title: `Error Creating Assistant: ${result.data?.message}`,
          subtitle: ''
        });
      }
    };
  }}
>
  <div class="container">
    <div class="inner-container">
      <div class="top-row">
        <div class="title">New Assistant</div>
        <AssistantAvatar bind:files bind:selectedPictogramName />
      </div>
      <TextInput
        name="name"
        labelText="Name"
        placeholder="Assistant name"
        on:keyup={handleChange}
        on:blur={handleChange}
        bind:value={$form.name}
        maxlength={ASSISTANTS_NAME_MAX_LENGTH}
      />
      {#if $errors.name}
        <small class="error">{$errors.name}</small>
      {/if}

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
        on:keyup={handleChange}
        on:blur={handleChange}
        bind:value={$form.description}
        maxlength={ASSISTANTS_DESCRIPTION_MAX_LENGTH}
      />

      {#if $errors.description}
        <small class="error">{$errors.description}</small>
      {/if}

      <InputTooltip
        name="instructions"
        labelText="Instructions"
        tooltipText="Detailed instructions to guide your assistant's responses and behavior"
      />

      <TextArea
        name="instructions"
        labelText="Instructions"
        on:keyup={handleChange}
        on:blur={handleChange}
        bind:value={$form.instructions}
        rows={6}
        placeholder="You'll act as..."
        hideLabel
        maxlength={ASSISTANTS_INSTRUCTIONS_MAX_LENGTH}
      />

      {#if $errors.instructions}
        <small class="error">{$errors.instructions}</small>
      {/if}

      <InputTooltip
        name="temperature"
        labelText="Temperature"
        tooltipText="Adjust the slider to set the creativity level of your assistant's responses"
      />
      <Slider
        name="temperature"
        on:click={handleSliderChange}
        bind:value={$form.temperature}
        hideLabel
        hideTextInput
        fullWidth
        min={0}
        max={1}
        step={0.1}
        minLabel="Min"
        maxLabel="Max"
      />

      {#if $errors.temperature}
        <small class="error">{$errors.temperature}</small>
      {/if}

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
        <Button kind="primary" size="small" type="submit" disabled={!$state.isValid}>Save</Button>
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

<style lang="scss">
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

  .error {
    color: themes.$text-error;
  }

  .cancel-modal {
    :global(.bx--modal-container) {
      position: absolute;
      top: 25%;
    }
  }
</style>
