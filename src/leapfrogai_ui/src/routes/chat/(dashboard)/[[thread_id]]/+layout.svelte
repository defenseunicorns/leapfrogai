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

  <main class="content chat-content">
    <slot />
  </main>
</div>

<style lang="scss">
  .chat-content {
    max-width: calc(
      100% - var(--sidebar-width)
    ); // prevents "random" shrinking of sidebar with some messages
  }
</style>
