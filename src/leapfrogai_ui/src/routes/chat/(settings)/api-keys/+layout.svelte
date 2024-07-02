<script lang="ts">
  import { page } from '$app/stores';
  import { Breadcrumb, BreadcrumbItem, Content } from 'carbon-components-svelte';
  import { threadsStore } from '$stores';

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

<Content>
  <div class="lf-content-container">
    <div class="slot-wrapper">
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
      <slot />
    </div>
  </div>
</Content>
