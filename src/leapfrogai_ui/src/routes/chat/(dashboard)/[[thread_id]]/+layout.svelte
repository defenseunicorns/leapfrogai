<script lang="ts">
  import { page } from '$app/stores';
  import threadsStore from '$stores/threads';
  import SidebarWrapper from '$components/SidebarWrapper.svelte';

  $: threadLabel = $threadsStore.threads.find((thread) => thread.id === $page.params.thread_id)
    ?.metadata.label;
</script>

<svelte:head>
  <title>{threadLabel || 'LeapfrogAI - Chat'}</title>
</svelte:head>

<div class="flex h-full">
  <SidebarWrapper />

  <main class="content lg:full-width-minus-sidebar max-w-full">
    <slot />
  </main>
</div>
