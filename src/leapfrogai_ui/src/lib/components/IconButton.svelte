<script lang="ts">
  import { twMerge } from 'tailwind-merge';

  export let btnClass =
    'dark:text-gray-400 dark:hover:text-white rounded-lg p-1 transition duration-100 ease-in-out';
</script>

<button type="button" {...$$restProps} class={twMerge(btnClass, $$props.class)} on:click>
  <slot />
</button>
