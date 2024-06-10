<script lang="ts">
  import { page } from '$app/stores';
  import threadsStore from '$stores/threads';
  import '../../../styles/main.scss';
  import { ChatSidebar } from '$components';
  import { Content } from 'carbon-components-svelte';

  $: innerWidth = 0;

  $: threadLabel = $threadsStore.threads.find((thread) => thread.id === $page.params.thread_id)
    ?.metadata.label;
</script>

<svelte:head>
  <title>{threadLabel || $page.data.title}</title>
</svelte:head>

<svelte:window bind:innerWidth />

<ChatSidebar />

<Content>
  <slot />
</Content>
