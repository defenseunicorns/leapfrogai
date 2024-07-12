<script lang="ts">
  import { Breadcrumb, BreadcrumbItem, Content } from 'carbon-components-svelte';
  import { page } from '$app/stores';
  import { PoweredByDU } from '$components';
  import { threadsStore } from '$stores';

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
    },
    {
      path: '/chat/assistants-management/edit',
      name: 'Edit Assistant'
    }
  ];

  $: isCurrentPage = (path: string) =>
    $page.url.pathname === path ||
    // Handle edit route with assistant id as path parameter
    ($page.url.pathname.startsWith('/chat/assistants-management/edit/') &&
      path === '/chat/assistants-management/edit');

  const getPath = (path: string) => {
    if (path === '/chat')
      return $threadsStore.lastVisitedThreadId
        ? `/chat/${$threadsStore.lastVisitedThreadId}`
        : '/chat';
    return path;
  };
</script>

<Content>
  <Breadcrumb noTrailingSlash>
    {#each paths as { path, name } (path)}
      {#if $page.url.pathname.includes(path)}
        <BreadcrumbItem
          href={isCurrentPage(path) ? '' : getPath(path)}
          isCurrentPage={isCurrentPage(path)}>{name}</BreadcrumbItem
        >
      {/if}
    {/each}
  </Breadcrumb>
  <div class="lf-content-container">
    <slot />

    <PoweredByDU />
  </div>
</Content>
