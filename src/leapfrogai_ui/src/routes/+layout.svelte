<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	// Gray 90 theme
	import { page } from '$app/stores';
	import 'carbon-components-svelte/css/g90.css';
	import '../styles/main.scss';
	import { Toasts } from '$components';

	export let data;

	let { supabase, session } = data;
	$: ({ supabase, session } = data);

	onMount(() => {
		const { data } = supabase.auth.onAuthStateChange((event, _session) => {
			if (_session?.expires_at !== session?.expires_at) {
				invalidate('supabase:auth');
			}
		});

		return () => data.subscription.unsubscribe();
	});
</script>

<svelte:head>
	<title>LeapfrogAI{$page.data.title ? ` - ${$page.data.title}` : ''}</title>
</svelte:head>

<Toasts />
<slot />
