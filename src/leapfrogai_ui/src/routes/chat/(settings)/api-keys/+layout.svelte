<script lang="ts">
  import { page } from '$app/stores';
  import { Breadcrumb, BreadcrumbItem, Content } from 'carbon-components-svelte';
  import { threadsStore } from '$stores';
  import { PoweredByDU } from '$components';
  import LayoutWithBreadcrumb from '$components/LayoutWithBreadcrumb.svelte';

  const paths = [
    {
      path: '/chat',
      name: 'Chat'
    },
    {
      path: '/chat/api-keys',
      name: 'API Keys'
    }
  ];

  $: isCurrentPage = (path: string) => $page.url.pathname === path;

  const getPath = (path: string) => {
    if (path === '/chat')
      return $threadsStore.lastVisitedThreadId
        ? `/chat/${$threadsStore.lastVisitedThreadId}`
        : '/chat';
    return path;
  };
</script>

<LayoutWithBreadcrumb {paths} {getPath}><slot /></LayoutWithBreadcrumb>
