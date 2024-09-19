<script lang="ts">
  import { onDestroy } from 'svelte';
  import ControlButton from 'flowbite-svelte/ControlButton.svelte';
  import { twMerge } from 'tailwind-merge';

  export let hidden = false;
  export let innerDivClass = '';

  let scrollContainerRef: HTMLDivElement;
  let resizeObserver: ResizeObserver;

  let hideButtons = true;

  const scrollLeft = () => {
    scrollContainerRef.scrollBy({
      left: -250,
      behavior: 'smooth'
    });
  };
  const scrollRight = () => {
    scrollContainerRef.scrollBy({
      left: 250,
      behavior: 'smooth'
    });
  };

  const checkOverflow = () => {
    if (scrollContainerRef) {
      // Check if the scroll container is overflowing horizontally
      const isOverflowing = scrollContainerRef.scrollWidth > scrollContainerRef.clientWidth;
      hideButtons = !isOverflowing; // Show/hide buttons based on overflow
    }
  };

  $: if (scrollContainerRef) {
    checkOverflow();
    scrollContainerRef.addEventListener('scroll', checkOverflow);

    resizeObserver = new ResizeObserver(() => {
      checkOverflow();
    });

    resizeObserver.observe(scrollContainerRef);
  }

  onDestroy(() => {
    if (scrollContainerRef) scrollContainerRef.removeEventListener('scroll', checkOverflow);
  });
</script>

<svelte:window on:resize={checkOverflow} />

{#if hidden}
  <slot />
{:else}
  <div class={twMerge('relative flex items-center gap-2')}>
    <ControlButton
      name="Previous"
      forward={false}
      on:click={scrollLeft}
      class={twMerge(hideButtons ? 'hidden' : 'static block p-0')}
    />

    <div
      bind:this={scrollContainerRef}
      class={twMerge('flex max-w-full overflow-x-auto bg-gray-700', innerDivClass)}
    >
      <slot />
    </div>
    <ControlButton
      name="Next"
      forward={true}
      on:click={scrollRight}
      class={twMerge(hideButtons ? 'hidden' : 'static block p-0')}
    />
  </div>
{/if}
