<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';
  import { page } from '$app/stores';
  import { Add, User } from 'carbon-icons-svelte';
  import { Button, Slider, TextArea, TextInput, Tooltip } from 'carbon-components-svelte';
  import TooltipTextInput from '$components/TooltipTextInput.svelte';

  export let form: ActionData;

  let name: string = '';
  let tagline: string = '';
  let instructions: string = '';
  let temperature: number = 0.5;

</script>

<form method="POST" action="?/newAssistant" use:enhance>
  <div class="container">
    <div class="inner-container">
      <div class="top-row">
        <div class="title">New Assistant</div>
        <button class="user-icon remove-btn-style" tabindex="0">
          <User />
        </button>
      </div>
      <TextInput name="name" labelText="Name" placeholder="Assistant name" bind:value={name} />
      {#if form?.errors?.name}
        <small class="error">{form.errors.name}</small>
      {/if}

      <TooltipTextInput
        name="tagline"
        labelText="Tagline"
        tooltipText="Taglines display on assistant tiles"
        placeholder="Here to help..."
        value={tagline}
      />
      {#if form?.errors?.tagline}
        <small class="error">{form.errors.tagline}</small>
      {/if}

      <TooltipTextInput
        labelText="Instructions"
        tooltipText="Detailed instructions to guide your assistant's responses and behavior"
        placeholder="You'll act as..."
      >
        <TextArea
          name="instructions"
          labelText="instructions"
          slot="input"
          bind:value={instructions}
          rows={6}
          placeholder="You'll act as..."
          hideLabel
        />
      </TooltipTextInput>
      {#if form?.errors?.instructions}
        <small class="error">{form.errors.instructions}</small>
      {/if}

      <TooltipTextInput
        labelText="Temperature"
        tooltipText="Adjust the slider to set the creativity level of your assistant's responses"
      >
        <Slider
          name="temperature"
          slot="input"
          bind:value={temperature}
          hideLabel
          hideTextInput
          fullWidth
          min={0}
          max={1}
          step={0.1}
          minLabel="Min"
          maxLabel="Max"
        />
      </TooltipTextInput>
      {#if form?.errors?.temperature}
        <small class="error">{form.errors.temperature}</small>
      {/if}

      <TooltipTextInput
        labelText="Data Sources"
        tooltipText="Specific files your assistant can search and reference"
      >
        <Button name="dataSources" slot="input" icon={Add} kind="secondary" size="small">Add</Button
        >
      </TooltipTextInput>

      <div>
        <Button kind="secondary" size="small">Cancel</Button>
        <Button kind="primary" size="small" type="submit">Save</Button>
      </div>
    </div>
  </div>
</form>

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

  .user-icon :global(svg) {
    width: 3rem;
    height: 3rem;
    padding: layout.$spacing-03;
    border-radius: 50%;
    background-color: themes.$layer-01;
    transition: background-color 70ms ease;
    &:hover {
      background-color: themes.$layer-02;
    }
  }

  .error {
    color: themes.$text-error;
  }
</style>
