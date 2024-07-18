<script lang="ts">
  import {
    Button,
    Input,
    Sidebar,
    SidebarDropdownWrapper,
    SidebarGroup,
    SidebarWrapper
  } from 'flowbite-svelte';
  import { PlusOutline } from 'flowbite-svelte-icons';
  import { dates } from '$helpers';
  import { threadsStore, uiStore } from '$stores';
  import type { LFThread } from '$lib/types/threads';
  import LFSidebarDropdownItem from '$components/LFSidebarDropdownItem.svelte';
  import { page } from '$app/stores';

  let searchText = '';
  let filteredThreads: LFThread[] = [];

  $: activeThreadId = $page.params.thread_id;
  $: organizedThreads = dates.organizeThreadsByDate(
    searchText !== '' ? filteredThreads : $threadsStore.threads
  );
</script>

<Sidebar class=" w-full max-w-64 overflow-y-auto">
  <SidebarWrapper class="no-scrollbar h-full">
    <SidebarGroup>
      <div class="flex flex-col gap-2">
        <Button on:click={() => threadsStore.changeThread('')}>
          <PlusOutline />New Chat
        </Button>
        <Input type="txt" placeholder="Search..." bind:value={searchText} maxlength={25}></Input>
      </div>
    </SidebarGroup>
    <SidebarGroup border>
      {#each organizedThreads as category}
        {#if category.threads.length > 0}
          <SidebarDropdownWrapper label={category.label} isOpen={true}>
            {#each category.threads as thread, index (thread.id)}
              <LFSidebarDropdownItem
                threadId={thread.id}
                label={thread.metadata.label}
                active={activeThreadId === thread.id}
              />
            {/each}
          </SidebarDropdownWrapper>
        {/if}
      {/each}
    </SidebarGroup>
  </SidebarWrapper>
</Sidebar>
