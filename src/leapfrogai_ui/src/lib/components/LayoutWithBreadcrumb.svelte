<script lang="ts">
  import { page } from '$app/stores';
  import { PoweredByDU } from '$components/index.js';
  import { Breadcrumb, BreadcrumbItem } from 'flowbite-svelte';

  export let paths: { path: string; name: string }[];
  export let getPath: (path: string) => string;
</script>

<main class="content">
  <Breadcrumb data-testid="breadcrumbs" aria-label="breadcrumbs" class="mb-4">
    {#each paths as { path, name } (path)}
      {#if $page.url.pathname.includes(path)}
        <BreadcrumbItem home={name === 'Chat'} href={getPath(path)}>{name}</BreadcrumbItem>
      {/if}
    {/each}
  </Breadcrumb>
  <div class="flex h-full justify-center overflow-auto">
    <div class="flex w-full flex-col items-center">
      <slot />
    </div>
  </div>
  <PoweredByDU />
</main>
