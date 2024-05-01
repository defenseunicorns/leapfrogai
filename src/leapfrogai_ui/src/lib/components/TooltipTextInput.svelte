<!--
This component turns off the Carbon Component Svelte TextInput's label and uses our own label
that includes a tooltip icon.

Slots:
- input: you can override this with your own component if desired
-->

<script lang="ts">
  import { TextInput, Tooltip } from 'carbon-components-svelte';

  export let labelText: string;
  export let tooltipText: string;
  export let placeholder: string = 'Type here';
  export let direction: 'top' | 'bottom' | 'left' | 'right' = 'right';
</script>

<div>
  <div class="label-and-tooltip">
    <label class="bx--label" style="margin-bottom: 0">{labelText}</label>
    <Tooltip {direction}>
      <p>{tooltipText}</p>
    </Tooltip>
  </div>
  <slot name="input">
    <TextInput {placeholder} hideLabel />
  </slot>
</div>

<style lang="scss">
  .label-and-tooltip {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-bottom: 0.5rem;
  }
</style>
