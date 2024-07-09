<script lang="ts">
  import { Copy } from 'carbon-icons-svelte';
  import { Button } from 'carbon-components-svelte';
  import { toastStore } from '$stores';

  export let value: string;
  export let toastTitle = 'Copied';
  export let btnText = 'Copy';
  export let size: 'small' | 'default' | 'field' | 'lg' | 'xl' | undefined = 'small';

  const handleClick = async () => {
    if (value) {
      await navigator.clipboard.writeText(value);
      toastStore.addToast({
        kind: 'info',
        title: toastTitle,
        subtitle: ''
      });
    }
  };
</script>

<Button kind="tertiary" icon={Copy} {size} on:click={handleClick}>{btnText}</Button>
