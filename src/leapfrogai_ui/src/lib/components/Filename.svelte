<script lang="ts">
  import { BanOutline, CheckOutline, CloseOutline } from 'flowbite-svelte-icons';
  import { Spinner } from 'flowbite-svelte';
  import IconButton from '$components/IconButton.svelte';

  export let status = 'uploading';
  export let invalid = false;
</script>

{#if status === 'uploading'}
  <Spinner color="gray" />
{/if}

{#if status === 'edit'}
  {#if invalid}
    <BanOutline tabindex="0" color="red" />
  {:else}
    <IconButton tabindex="0" on:click on:keydown>
      <CloseOutline />
    </IconButton>
  {/if}
{/if}

{#if status === 'complete'}
  <CheckOutline tabindex="0" color="green" />
{/if}
