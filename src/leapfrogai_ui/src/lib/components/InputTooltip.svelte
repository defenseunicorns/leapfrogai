<script lang="ts">
  import { Tooltip } from 'carbon-components-svelte';

  export let name: string = '';
  export let labelText: string;
  export let tooltipText: string;
  export let direction: 'top' | 'bottom' | 'left' | 'right' = 'right';
</script>

<div class="label-and-tooltip">
  <label for={name} class="bx--label" style="margin-bottom: 0">{labelText}</label>
  <Tooltip {direction}>
    <p>{tooltipText}</p>
  </Tooltip>
</div>

<style lang="scss">
  .label-and-tooltip {
    display: flex;
    justify-content: flex-start;
    align-items: center;
  }
</style>
