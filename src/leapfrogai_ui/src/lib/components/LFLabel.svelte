<script lang="ts">
  import { Label } from 'flowbite-svelte';
  import InfoTooltip from '$components/InfoTooltip.svelte';
  import { twMerge } from 'tailwind-merge';

  export let id: string;
  export let labelClass: string = '';
  export let tooltipText: string | undefined = undefined;

  let labelInnerClass = twMerge('block', labelClass);
</script>

<div class={twMerge('mb-3 flex gap-2', $$props.class)}>
  <Label for={id} class={labelInnerClass}><slot /></Label>
  {#if tooltipText}
    <InfoTooltip>{tooltipText}</InfoTooltip>
  {/if}
</div>
