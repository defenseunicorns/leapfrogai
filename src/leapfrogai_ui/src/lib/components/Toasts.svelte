<script lang="ts">
  import { toastStore } from '$stores';
  import { slide } from 'svelte/transition';
  import LFToast from '$components/Toasts/LFToast.svelte';
</script>

{#if $toastStore.toasts}
  <section class="absolute right-0 top-header z-50 flex flex-col justify-center gap-1">
    {#each $toastStore.toasts as toast (toast.id)}
      <div transition:slide>
        <LFToast {toast} />
      </div>
    {/each}
  </section>
{/if}
