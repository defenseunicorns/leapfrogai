<script lang="ts">
  import { Breadcrumb, BreadcrumbItem } from 'flowbite-svelte';
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

  const getPath = (path: string) => {
    if (path === '/chat')
      return $threadsStore.lastVisitedThreadId
        ? `/chat/${$threadsStore.lastVisitedThreadId}`
        : '/chat';
    return path;
  };
</script>

<main class="content">
  <div class="flex h-full justify-center overflow-auto">
    <div class="flex w-3/4 flex-col">
      <Breadcrumb data-testid="breadcrumbs" aria-label="breadcrumbs">
        {#each paths as { path, name } (path)}
          {#if $page.url.pathname.includes(path)}
            <BreadcrumbItem home={name === 'Chat'} href={getPath(path)}>{name}</BreadcrumbItem>
          {/if}
        {/each}
      </Breadcrumb>
      <slot />
    </div>
  </div>
  <PoweredByDU />
</main>
