<script lang="ts">
  import { Add, User } from 'carbon-icons-svelte';
  import { Button, Slider, TextArea, TextInput, Tooltip } from 'carbon-components-svelte';
  import TooltipTextInput from '$components/TooltipTextInput.svelte';
</script>

<div class="container">
  <div class="inner-container">
    <div class="top-row">
      <div class="title">New Assistant</div>
      <button class="user-icon remove-btn-style" tabindex="0">
        <User />
      </button>
    </div>
    <TextInput labelText="Name" placeholder="Assistant name" />

    <TooltipTextInput
      labelText="Tagline"
      tooltipText="Taglines display on assistant tiles"
      placeholder="Here to help..."
    />

    <TooltipTextInput
      labelText="Instructions"
      tooltipText="Detailed instructions to guide your assistant's responses and behavior"
      placeholder="You'll act as..."
    >
      <TextArea
        labelText="instructions"
        slot="input"
        rows={6}
        placeholder="You'll act as..."
        hideLabel
      />
    </TooltipTextInput>

    <TooltipTextInput
      labelText="Temperature"
      tooltipText="Adjust the slider to set the creativity level of your assistant's responses"
    >
      <Slider
        slot="input"
        labelText="temperature"
        hideLabel
        hideTextInput
        fullWidth
        value={1}
        min={0}
        max={2}
        step={0.1}
        minLabel="Min"
        maxLabel="Max"
      />
    </TooltipTextInput>

    <TooltipTextInput
      labelText="Data Sources"
      tooltipText="Specific files your assistant can search and reference"
    >
      <Button slot="input" icon={Add} kind="secondary" size="small">Add</Button>
    </TooltipTextInput>

    <div>
      <Button kind="secondary" size="small">Cancel</Button>
      <Button kind="primary" size="small">Save</Button>
    </div>
  </div>
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

  .user-icon :global(svg) {
    width: 3rem;
    height: 3rem;
    padding: layout.$spacing-03;
    border-radius: 50%;
    background-color: themes.$layer-01;
  }
</style>
