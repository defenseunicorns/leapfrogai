<script lang="ts">
  import { Breadcrumb, BreadcrumbItem, Content } from 'carbon-components-svelte';
  import { page } from '$app/stores';
  import { PoweredByDU } from '$components';

  const paths = [
    {
      path: '/chat',
      name: 'Chat'
    },
    {
      path: '/chat/file-management',
      name: 'File Management'
    }
  ];
  $: isCurrentPage = (path: string) => $page.url.pathname === path;
</script>

<Content>
  <div class="lf-content-container">
    <div class="slot-wrapper">
      <Breadcrumb noTrailingSlash>
        {#each paths as { path, name } (path)}
          {#if $page.url.pathname.includes(path)}
            <BreadcrumbItem
              href={isCurrentPage(path) ? '' : path}
              isCurrentPage={isCurrentPage(path)}>{name}</BreadcrumbItem
            >
          {/if}
        {/each}
      </Breadcrumb>
      <slot />
    </div>

    <PoweredByDU />
  </div>
</Content>

<style lang="scss">
  .slot-wrapper {
    height: 100%;
  }
  .lf-content-container {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
