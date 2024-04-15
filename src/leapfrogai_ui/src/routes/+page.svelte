<script lang="ts">
	import logo from '$assets/LeapfrogAI.png';
	import { goto } from '$app/navigation';
	import { Button } from 'carbon-components-svelte';

	export let data;
	export let queryParams: { [key: string]: string } | undefined = undefined;

	let { session } = data;
	$: ({ session } = data);

	$: if (session?.user) {
		goto('/chat');
	}

	async function signInWithKeycloak() {
		await data.supabase.auth.signInWithOAuth({
			provider: 'keycloak',
			options: {
				scopes: 'openid',
				redirectTo: `${data.url}/auth/callback`,
				queryParams
			}
		});
	}
</script>

<div class="login-container">
	<div class="logo">
		<img alt="LeapfrogAI Logo" src={logo} class="logo" />
	</div>
	<Button on:click={signInWithKeycloak} kind="secondary">Log In with UDS SSO</Button>
</div>

<style lang="scss">
	.logo {
		width: 252px;
		height: 72px;
	}
	.login-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: layout.$spacing-08;
		width: 100%;
		padding-top: layout.$spacing-04;
	}
</style>
