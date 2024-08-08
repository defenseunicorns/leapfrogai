<script lang="ts">
  import { twMerge } from 'tailwind-merge';
  interface Sizes {
    [key: string]: string;
  }

  const sizes: Sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    xxl: 'max-w-2xl'
  };

  export let divClass: string =
    'flex justify-center items-center h-56 bg-gray-300 rounded-lg animate-pulse dark:bg-gray-700';
  export let size: keyof Sizes = 'sm';
  $: outDivclass = twMerge(sizes[size], divClass, $$props.class);
</script>

<div role="status" class={outDivclass} {...$$restProps}>
  <svg
    class="h-12 w-12 text-gray-200 dark:text-gray-600"
    aria-hidden="true"
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      fill-rule="evenodd"
      d="M9 2.221V7H4.221a2 2 0 0 1 .365-.5L8.5 2.586A2 2 0 0 1 9 2.22ZM11 2v5a2 2 0 0 1-2 2H4v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2h-7Z"
      clip-rule="evenodd"
    />
  </svg>

  <span class="sr-only">Loading...</span>
</div>
