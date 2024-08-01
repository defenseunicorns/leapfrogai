<script lang="ts">
  import { toastStore } from '$stores';
  import { slide } from 'svelte/transition';
  import LFToast from '$components/LFToast.svelte';
</script>

{#if $toastStore.toasts}
  <section class="max-z absolute right-0 top-header flex flex-col justify-center gap-1">
    {#each $toastStore.toasts as toast (toast.id)}
      <div transition:slide>
        <LFToast {toast} />
      </div>
    {/each}
  </section>
{/if}

<style>
  .max-z {
    z-index: 9999; /* Flowbite uses z-50 for modals, we want toasts above that */
  }
</style>
