<script lang="ts">
  import { threadsStore } from '$stores';
  import LayoutWithBreadcrumb from '$components/LayoutWithBreadcrumb.svelte';

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

<LayoutWithBreadcrumb {paths} {getPath}><slot /></LayoutWithBreadcrumb>
