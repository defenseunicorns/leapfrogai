<script lang="ts">
  import { twMerge } from 'tailwind-merge';

  export let btnClass = 'dark:text-gray-400 dark:hover:text-white rounded-lg p-1';
</script>

<button
  type="button"
  {...$$restProps}
  class={twMerge(btnClass, $$props.class)}
  on:click
  on:change
  on:keydown
  on:keyup
  on:touchstart|passive
  on:touchend
  on:touchcancel
  on:mouseenter
  on:mouseleave
>
  <slot />
</button>
