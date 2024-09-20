<script lang="ts">
  import { onDestroy } from 'svelte';
  import { twMerge } from 'tailwind-merge';
  import LFControlButton from '$components/LFControlButton.svelte';

  export let hidden = false;
  export let innerDivClass = '';
  export let scrollAmount = 250;
  export let btnHeight = null;
  export let btnWidth = null;

  let scrollContainerRef: HTMLDivElement;
  let resizeObserver: ResizeObserver;

  let canScrollLeft = false;
  let canScrollRight = false;

  let isOverflowing = false;

  const scrollLeft = () => {
    scrollContainerRef.scrollBy({
      left: scrollAmount * -1,
      behavior: 'smooth'
    });
  };
  const scrollRight = () => {
    scrollContainerRef.scrollBy({
      left: scrollAmount,
      behavior: 'smooth'
    });
  };

  const checkOverflow = () => {
    if (scrollContainerRef) {
      // Check if the scroll container is overflowing horizontally
      isOverflowing = scrollContainerRef.scrollWidth > scrollContainerRef.clientWidth;

      const scrollLeftPos = scrollContainerRef.scrollLeft;
      const maxScrollLeft = scrollContainerRef.scrollWidth - scrollContainerRef.clientWidth;

      // Check if the container can scroll left or right
      canScrollLeft = scrollLeftPos > 0;
      canScrollRight = scrollLeftPos < maxScrollLeft;
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
  <slot {...$$props} />
{:else}
  <div
    class={twMerge(
      'relative flex items-center gap-1',
      !canScrollLeft && 'ml-7',
      !canScrollRight && 'me-7'
    )}
    {...$$props}
  >
    <LFControlButton
      name="Previous"
      forward={false}
      on:click={scrollLeft}
      class={twMerge(!canScrollLeft ? 'hidden' : 'static block p-0')}
      {btnHeight}
      {btnWidth}
    />

    <div
      bind:this={scrollContainerRef}
      data-testid="scroll-container"
      class={twMerge(
        'flex max-w-full flex-col overflow-x-auto bg-gray-700',
        !isOverflowing && 'mb-[15px]',
        innerDivClass
      )}
    >
      <slot />
    </div>
    <LFControlButton
      name="Next"
      forward={true}
      on:click={scrollRight}
      class={twMerge(!canScrollRight ? 'hidden' : 'static block p-0')}
      {btnHeight}
      {btnWidth}
    />
  </div>
{/if}
