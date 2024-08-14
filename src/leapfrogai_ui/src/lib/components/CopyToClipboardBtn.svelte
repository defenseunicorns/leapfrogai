<script lang="ts">
  import { Button } from 'flowbite-svelte';
  import { toastStore } from '$stores';
  import { FileCopyOutline } from 'flowbite-svelte-icons';
  import { twMerge } from 'tailwind-merge';

  export let value: string;
  export let toastTitle = 'Copied';
  export let btnText = '';
  export let size: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | undefined = 'sm';
  export let testId: string = 'copy-to-clipboard-btn';

  const handleClick = async (e) => {
    e.stopPropagation();
    if (value) {
      await navigator.clipboard.writeText(value);
      toastStore.addToast({
        kind: 'info',
        title: toastTitle
      });
    }
  };
</script>

<Button
  data-testid={testId}
  color="alternative"
  {size}
  on:click={handleClick}
  class={twMerge('dark:text-white', $$props.class)}>{btnText}<FileCopyOutline /></Button
>
