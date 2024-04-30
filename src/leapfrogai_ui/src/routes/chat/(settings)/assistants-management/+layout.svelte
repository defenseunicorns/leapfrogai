<script lang="ts">
	import { Breadcrumb, BreadcrumbItem } from 'carbon-components-svelte';
</script>

<Breadcrumb noTrailingSlash>
	<BreadcrumbItem href="/chat">Chat</BreadcrumbItem>
	<BreadcrumbItem href="/chat/assistants-management" isCurrentPage
		>Assistants Management</BreadcrumbItem
	>
</Breadcrumb>

<slot />
