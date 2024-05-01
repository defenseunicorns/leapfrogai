<script lang="ts">
  import { User } from 'carbon-icons-svelte';
  import { TextArea, TextInput, Tooltip } from 'carbon-components-svelte';
  import TooltipTextInput from '$components/TooltipTextInput.svelte';
</script>

<div class="container">
  <div class="inner-container">
    <div class="centered-flexbox">
      <div class="title">New Assistant</div>
      <div class="user-icon">
        <User />
      </div>
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
      <TextArea slot="input" rows={6} placeholder="You'll act as..."/>
    </TooltipTextInput>
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
    gap: 1rem;
    width: 50%;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
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
