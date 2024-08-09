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

  export let divClass: string = 'animate-pulse';
  export let size: keyof Sizes = 'sm';
  export let darkColor = 'bg-gray-700';
  export let lightColor = 'bg-gray-200';
  $: outDivclass = twMerge(sizes[size], divClass, $$props.class);
</script>

<div role="status" class={outDivclass} {...$$restProps}>
  <div class={`h-2 ${lightColor} mb-2.5 rounded-full dark:${darkColor}`}></div>
  <div class={`h-2 ${lightColor} mb-2.5 w-10/12 rounded-full dark:${darkColor}`}></div>
  <span class="sr-only">Loading...</span>
</div>
