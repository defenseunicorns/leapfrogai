<script lang="ts">
	import { uiStore } from '$stores';
	import logo from '$assets/LeapfrogAI.png';
	import { Settings, UserAvatar } from 'carbon-icons-svelte';
	import { Header, HeaderAction, HeaderUtilities } from 'carbon-components-svelte';

	let loading = false;
	let signOutForm: HTMLFormElement;

	$: innerWidth = 0;

	const handleLogOut = () => {
		loading = true;
		signOutForm.submit();
		loading = false;
	};

	// We override the default behavior of the HeaderAction component to close other actions
	// when a new one is opened
	let activeHeaderAction: { [key: string]: boolean };
	$: activeHeaderAction = {
		user: false,
		settings: false
	};

	const setActiveHeaderAction = (headerActionName: keyof typeof activeHeaderAction) => {
		Object.keys(activeHeaderAction).forEach((key) => {
			activeHeaderAction[key] = key === headerActionName;
		});
	};
</script>

<svelte:window bind:innerWidth />

<Header
	persistentHamburgerMenu={innerWidth ? innerWidth < 1056 : false}
	bind:isSideNavOpen={$uiStore.isSideNavOpen}
>
	<span slot="platform"><img alt="LeapfrogAI Logo" src={logo} class="logo" /></span>
	<HeaderUtilities>
		<HeaderAction
			data-testid="settings header action button"
			aria-label="Settings"
			title="Settings"
			icon={Settings}
			transition={false}
			isOpen={activeHeaderAction.settings}
			on:open={() => setActiveHeaderAction('settings')}
		>
			<div class="link-container">
				<a
					href="/chat/assistants-management"
					class="header-link"
					on:click={() => setActiveHeaderAction('')}>Assistants Management</a
				>
			</div>
		</HeaderAction>
		<HeaderAction
			data-testid="user header action button"
			aria-label="User"
			title="User"
			icon={UserAvatar}
			transition={false}
			isOpen={activeHeaderAction.user}
			on:open={() => setActiveHeaderAction('user')}
		>
			<div class="link-container">
				<form bind:this={signOutForm} method="post" action="/auth?/signout">
					<button
						class="header-link"
						aria-label="Log Out"
						disabled={loading}
						on:click={handleLogOut}>Log Out</button
					>
				</form>
			</div>
		</HeaderAction>
	</HeaderUtilities>
</Header>

<style lang="scss">
	.logo {
		width: 126px;
		height: 36px;
	}

	.link-container {
		padding: layout.$spacing-05;
	}

	.header-link {
		@include type.type-style('heading-compact-01');
		cursor: pointer;
		background: none;
		color: inherit;
		border: none;
		padding: 0;
		outline: inherit;
		text-decoration: none;
		&:hover {
			color: themes.$text-on-color;
		}
	}
</style>
