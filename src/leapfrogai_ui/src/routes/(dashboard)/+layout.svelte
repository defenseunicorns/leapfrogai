<script lang="ts">
	import { Content, Header, HeaderAction, HeaderUtilities, Theme } from 'carbon-components-svelte';
	import UserAvatar from 'carbon-icons-svelte/lib/UserAvatar.svelte';
	import { page } from '$app/stores';
	import logo from '$assets/LeapfrogAI.png';
	import type { CarbonTheme } from 'carbon-components-svelte/src/Theme/Theme.svelte';
	import { conversationsStore } from '$stores';
	import '../../styles/main.scss';
	import { ChatSidebar } from '$components';
	import { onMount } from 'svelte';

	let theme: CarbonTheme | undefined = 'g90';
	let loading = false;
	let signOutForm: HTMLFormElement;
	let isSideNavOpen = true;
	$: innerWidth = 0;

	$: conversationLabel = $conversationsStore.conversations.find(
		(conversation) => conversation.id === $page.params.conversation_id
	)?.label;

	const handleLogOut = () => {
		loading = true;
		signOutForm.submit();
		loading = false;
	};

	onMount(() => {
		// When trying to set the isSideNavOpen to true when initialized as a variable
		// Header component overrides it to false so menu closes, setting to true here
		// to prevent that
		isSideNavOpen = true;
	});

</script>

<svelte:head>
	<title>{conversationLabel || $page.data.title}</title>
</svelte:head>

<svelte:window bind:innerWidth />

<Theme bind:theme />

<Header persistentHamburgerMenu={innerWidth ? innerWidth < 1056 : false} bind:isSideNavOpen>
	<span slot="platform"><img alt="LeapfrogAI Logo" src={logo} class="logo" /></span>
	<HeaderUtilities>
		<HeaderAction aria-label="User" title="User" icon={UserAvatar}>
			<div class="link-container">
				<form bind:this={signOutForm} method="post" action="/auth?/signout">
					<button class="logout-btn" aria-label="Log Out" disabled={loading} on:click={handleLogOut}
						>Log Out</button
					>
				</form>
			</div>
		</HeaderAction>
	</HeaderUtilities>
</Header>
<ChatSidebar bind:isSideNavOpen />

<Content>
	<slot />
</Content>

<style lang="scss">
	:global(.bx--content) {
		height: calc(100vh - var(--header-height));
	}

	.logo {
		width: 126px;
		height: 36px;
	}

	.link-container {
		padding: layout.$spacing-05;
	}

	.logout-btn {
		@include type.type-style('heading-compact-01');
		cursor: pointer;
		background: none;
		color: inherit;
		border: none;
		padding: 0;
		outline: inherit;
		&:hover {
			color: themes.$text-on-color;
		}
	}

	:global(.bx--side-nav__item) {
		list-style-type: none;
	}
</style>
