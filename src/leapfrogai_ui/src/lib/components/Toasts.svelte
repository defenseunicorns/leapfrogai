<script lang="ts">
  import { toastStore } from '$stores';
  import { slide } from 'svelte/transition';
  import LFToast from '$components/LFToast.svelte';
  import AssistantProgressToast from '$components/AssistantProgressToast.svelte';
</script>

{#if $toastStore.toasts}
  <section
    class="z-max-1 max-height-sidebar-height absolute right-0 top-header flex flex-col gap-1 overflow-y-auto overflow-x-hidden"
  >
    {#each $toastStore.toasts as toast (toast.id)}
      <div transition:slide>
        {#if toast.variant === 'assistant-progress'}
          <AssistantProgressToast {toast} />
        {:else}
          <LFToast {toast} />
        {/if}
      </div>
    {/each}
  </section>
{/if}
