<script lang="ts">
  import { fade } from 'svelte/transition';
  import { twMerge } from 'tailwind-merge';
  import { ChevronLeftOutline, ChevronRightOutline } from 'flowbite-svelte-icons';
  import { STANDARD_FADE_DURATION } from '$constants';

  export let forward: boolean;
  export let name: string;
  export let btnHeight = 8;
  export let btnWidth = 8;

  let buttonCls: string;
  $: buttonCls = twMerge(
    'flex top-0 z-30 justify-center items-center px-4 h-full group focus:outline-none text-white dark:text-gray-300',
    forward ? 'end-0' : 'start-0',
    $$props.class
  );
</script>

<button
  on:click
  type="button"
  class={buttonCls}
  in:fade={{ duration: STANDARD_FADE_DURATION }}
  out:fade={{ duration: STANDARD_FADE_DURATION }}
>
  <slot>
    <span
      class={`inline-flex items-center justify-center w-${btnWidth} h-${btnHeight} group-hover:bg-white/50 group-focus:outline-none dark:group-hover:bg-gray-800/60 dark:group-focus:ring-gray-800/70`}
    >
      {#if forward}
        <ChevronRightOutline class="h-4 w-4" />
      {:else}
        <ChevronLeftOutline class="h-4 w-4" />
      {/if}
      <span class="sr-only">{name}</span>
    </span>
  </slot>
</button>
