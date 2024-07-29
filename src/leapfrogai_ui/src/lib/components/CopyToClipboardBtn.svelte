<script lang="ts">
  import { Button } from 'flowbite-svelte';
  import { toastStore } from '$stores';
  import { FileCopyOutline } from 'flowbite-svelte-icons';

  export let value: string;
  export let toastTitle = 'Copied';
  export let btnText = '';
  export let size: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | undefined = 'sm';
  export let testId: string;

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

<Button data-testid={testId} color="alternative" {size} on:click={handleClick}
  >{btnText}<FileCopyOutline /></Button
>
