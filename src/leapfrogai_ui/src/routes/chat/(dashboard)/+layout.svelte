<script lang="ts">
  import { page } from '$app/stores';
  import { conversationsStore } from '$stores';
  import '../../../styles/main.scss';
  import { ChatSidebar } from '$components';
  import LFContent from '$components/LFContent.svelte';

  $: innerWidth = 0;

  $: conversationLabel = $conversationsStore.conversations.find(
    (conversation) => conversation.id === $page.params.conversation_id
  )?.label;
</script>

<svelte:head>
  <title>{conversationLabel || $page.data.title}</title>
</svelte:head>

<svelte:window bind:innerWidth />

<ChatSidebar />

<LFContent><slot /></LFContent>
