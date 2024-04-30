<script lang="ts">
	import { page } from '$app/stores';
	import { conversationsStore } from '$stores';
	import { Content } from 'carbon-components-svelte';
	import '../../../styles/main.scss';
	import { ChatSidebar } from '$components';

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

<Content>
	<slot />
</Content>

<style lang="scss">
	:global(.bx--side-nav__item) {
		list-style-type: none;
	}
</style>
