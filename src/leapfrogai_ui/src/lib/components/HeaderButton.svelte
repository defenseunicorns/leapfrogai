<script lang="ts">
  import { twMerge } from 'tailwind-merge';

  export let btnClass =
    'dark:text-gray-400 hover:bg-secondary-800 dark:hover:bg-secondary-300 dark:hover:text-white rounded-lg p-1 focus:outline-none focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-300 transition duration-100 ease-in-out';
</script>

<button type="button" {...$$restProps} class={twMerge(btnClass, $$props.class)} on:click>
  <slot />
</button>
