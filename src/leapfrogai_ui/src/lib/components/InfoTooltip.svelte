<script lang="ts">
  import { Tooltip } from 'flowbite-svelte';
  import { InfoCircleOutline } from 'flowbite-svelte-icons';
  import { twMerge } from 'tailwind-merge';

  export let iconClass: string = '';
  export let tooltipClass: string = '';
</script>

<div class={$$props.class}>
  <InfoCircleOutline class={twMerge('text-gray-900 dark:text-gray-300', iconClass)} />
  <Tooltip data-testid="tooltip" placement="right" class={tooltipClass} {...$$restProps}
    ><slot /></Tooltip
  >
</div>
