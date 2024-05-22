<script lang="ts">
  import { page } from '$app/stores';
  import { threadsStore } from '$stores';
  import '../../../styles/main.scss';
  import { ChatSidebar } from '$components';
  import LFContent from '$components/LFContent.svelte';

  $: innerWidth = 0;

  $: threadLabel = $threadsStore.threads.find((thread) => thread.id === $page.params.thread_id)
    ?.metadata.label;
</script>

<svelte:head>
  <title>{threadLabel || $page.data.title}</title>
</svelte:head>

<svelte:window bind:innerWidth />

<ChatSidebar />

<LFContent><slot /></LFContent>
