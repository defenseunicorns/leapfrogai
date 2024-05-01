<script lang="ts">
  import { createForm } from 'svelte-forms-lib';
  import { Add, User } from 'carbon-icons-svelte';
  import { Button, Slider, TextArea, TextInput } from 'carbon-components-svelte';
  import TooltipTextInput from '$components/TooltipTextInput.svelte';
  import * as yup from 'yup';

  // TODO - cancel modal
  // TODO - tests

  const NewAssistantSchema = yup.object({
    name: yup.string().required('Required'),
    tagline: yup.string().required('Required'),
    instructions: yup.string().required('Required'),
    temperature: yup.number().required('Required'),
    dataSources: yup.array().of(yup.string())
  });

  const { form, errors, handleChange, handleSubmit } = createForm({
    initialValues: {
      name: '',
      tagline: '',
      instructions: '',
      temperature: 0.5
    },
    validationSchema: NewAssistantSchema,
    onSubmit: async (values) => {
      console.log(JSON.stringify(values));
      // TODO save to db
    }
  });
</script>

<form on:submit={handleSubmit}>
  <div class="container">
    <div class="inner-container">
      <div class="top-row">
        <div class="title">New Assistant</div>
        <!--Note - Avatar is a placeholder and will be completed in a future story-->
        <button class="user-icon remove-btn-style" tabindex="0" on:click|preventDefault>
          <User />
        </button>
      </div>
      <TextInput
        name="name"
        labelText="Name"
        placeholder="Assistant name"
        on:keyup={handleChange}
        on:blur={handleChange}
        bind:value={$form.name}
      />
      {#if $errors.name}
        <small class="error">{$errors.name}</small>
      {/if}

      <TooltipTextInput
        name="tagline"
        labelText="Tagline"
        tooltipText="Taglines display on assistant tiles"
        placeholder="Here to help..."
        on:keyup={handleChange}
        on:blur={handleChange}
        bind:value={$form.tagline}
      />
      {#if $errors.tagline}
        <small class="error">{$errors.tagline}</small>
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
          on:keyup={handleChange}
          on:blur={handleChange}
          bind:value={$form.instructions}
          rows={6}
          placeholder="You'll act as..."
          hideLabel
        />
      </TooltipTextInput>
      {#if $errors.instructions}
        <small class="error">{$errors.instructions}</small>
      {/if}

      <TooltipTextInput
        labelText="Temperature"
        tooltipText="Adjust the slider to set the creativity level of your assistant's responses"
      >
        <Slider
          name="temperature"
          slot="input"
          on:click={handleChange}
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
      </TooltipTextInput>
      {#if $errors.temperature}
        <small class="error">{$errors.temperature}</small>
      {/if}

      <!--Note - Data Sources is a placeholder and will be completed in a future story-->
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
