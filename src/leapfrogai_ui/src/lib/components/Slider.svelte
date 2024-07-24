<!-- A basic reference custom range component -->
<!-- Featuring: onChange events, Custom property theming, Tooltip, A11y keyboard controls + attributes, -->

<script lang="ts">
  import Range from '$components/Range.svelte';
  import LFLabel from '$components/LFLabel.svelte';

  export let id: string;
  export let label: string | undefined = undefined;
  export let tooltipText: string | undefined = undefined;
  export let max = 100;
  export let min = 0;
  export let value: number = Math.floor((max - min) / 2);
  export let showThumb = true;

  function normalize(value: number) {
    return (value - min) / (max - min);
  }
</script>

<div class="theme">
  {#if label}
    <LFLabel {id} {tooltipText}>{label}</LFLabel>
  {/if}
  <Range on:change={(e) => (value = normalize(e.detail.value))} {id} {max} {min} {showThumb} />
</div>

<style>
  .theme {
    --track-focus: #1e40af;
    --track-highlight-bgcolor: #1e40af;
    --track-highlight-bg: linear-gradient(90deg, #93c5fd, #1e3a8a);
    --thumb-holding-outline: #3b82f6;
    --tooltip-bgcolor: #374151;
    --tooltip-bg: #374151;
  }
</style>
