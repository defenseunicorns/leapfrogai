<!--
This is a modified version of Flowbite Svelte's Drawer.svelte component.
It allows adding custom styling to the backdrop (div with role "presentation")
-->

<script lang="ts">
  import { twMerge } from 'tailwind-merge';
  import { blur, fade, fly, slide } from 'svelte/transition';

  import type { drawerTransitionParamTypes, drawerTransitionTypes } from 'flowbite-svelte';
  import { clickOutside } from '$lib/utils/clickOutside';

  export let activateClickOutside: boolean = true;
  export let hidden: boolean = true;
  export let position: 'fixed' | 'absolute' = 'fixed';
  export let leftOffset: string = 'inset-y-0 start-0';
  export let rightOffset: string = 'inset-y-0 end-0';
  export let topOffset: string = 'inset-x-0 top-0';
  export let bottomOffset: string = 'inset-x-0 bottom-0';
  export let width: string = 'w-80';
  export let backdrop: boolean = true;
  export let bgColor: string = 'bg-gray-900';
  export let bgOpacity: string = 'bg-opacity-75';
  export let placement: 'left' | 'right' | 'top' | 'bottom' = 'left';
  export let id: string = 'drawer-example';
  export let divClass: string = 'overflow-y-auto z-50 p-4 bg-white dark:bg-gray-800';
  export let backdropCustomClass: string = '';
  export let transitionParams: drawerTransitionParamTypes = {};
  export let transitionType: drawerTransitionTypes = 'fly';

  function multiple(node: HTMLElement, params: drawerTransitionParamTypes) {
    switch (transitionType) {
      case 'slide':
        return slide(node, params);
      case 'blur':
        return blur(node, params);
      case 'fade':
        return fade(node, params);
      default:
        return fly(node, params);
    }
  }

  const placements = {
    left: leftOffset,
    right: rightOffset,
    top: topOffset,
    bottom: bottomOffset
  };

  const handleDrawer = () => {
    hidden = !hidden;
  };

  const handleClickOutside = () => activateClickOutside && !hidden && handleDrawer();

  let backdropDivClass = twMerge(
    'fixed top-0 start-0 z-50 w-full h-full',
    backdrop && bgColor,
    backdrop && bgOpacity,
    backdropCustomClass
  );

  function clickOutsideWrapper(node: HTMLElement, callback: () => void) {
    return activateClickOutside ? clickOutside(node, callback) : undefined;
  }
</script>

{#if !hidden}
  {#if backdrop && activateClickOutside}
    <div
      role="presentation"
      class={backdropDivClass}
      on:click={() => !hidden && handleDrawer()}
    ></div>
  {:else if backdrop && !activateClickOutside}
    <div role="presentation" class={backdropDivClass}></div>
  {/if}

  <div
    use:clickOutsideWrapper={handleClickOutside}
    {id}
    {...$$restProps}
    class={twMerge(divClass, width, position, placements[placement], $$props.class)}
    transition:multiple={transitionParams}
    tabindex="-1"
    aria-controls={id}
    aria-labelledby={id}
  >
    <slot {hidden}></slot>
  </div>
{/if}
