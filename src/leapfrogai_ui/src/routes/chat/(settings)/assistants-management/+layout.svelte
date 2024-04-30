<script lang="ts">
	import { Breadcrumb, BreadcrumbItem } from 'carbon-components-svelte';
	import { page } from '$app/stores';

	const paths = [
		{
			path: '/chat',
			name: 'Chat'
		},
		{
			path: '/chat/assistants-management',
			name: 'Assistants Management'
		},
		{
			path: '/chat/assistants-management/new',
			name: 'New Assistant'
		}
	];

	// TODO - test the breadcrumbs
</script>

<Breadcrumb noTrailingSlash>
	{#each paths as { path, name } (path)}
		{#if $page.url.pathname.includes(path)}
			<BreadcrumbItem href={path} isCurrentPage={$page.url.pathname === path}
				>{name}</BreadcrumbItem
			>
		{/if}
	{/each}
</Breadcrumb>

<slot />
