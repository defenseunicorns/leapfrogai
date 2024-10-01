<script lang="ts">
  import {
    Button,
    Hr,
    Input,
    Sidebar,
    SidebarDropdownWrapper,
    SidebarGroup,
    SidebarWrapper
  } from 'flowbite-svelte';
  import { PlusOutline } from 'flowbite-svelte-icons';
  import { dates } from '$helpers';
  import { threadsStore } from '$stores';
  import type { LFThread } from '$lib/types/threads';
  import LFSidebarDropdownItem from '$components/LFSidebarDropdownItem.svelte';
  import { page } from '$app/stores';
  import { getMessageText } from '$helpers/threads';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import ImportExport from '$components/ImportExport.svelte';

  let searchText = '';
  let filteredThreads: LFThread[] = [];
  let searchResults: FuseResult<LFThread>[];

  const options: IFuseOptions<unknown> = {
    keys: ['metadata.label', 'messages.content'],
    minMatchCharLength: 3,
    shouldSort: false,
    findAllMatches: true,
    threshold: 0, // perfect matches only
    ignoreLocation: true
  };

  $: activeThreadId = $page.params.thread_id;
  $: organizedThreads = dates.organizeThreadsByDate(
    searchText !== '' ? filteredThreads : $threadsStore.threads
  );

  $: if (searchText) {
    // Remap the message content to be a string instead of string | nested object
    const threadsWithTextMessages = $threadsStore.threads.map((thread) => ({
      ...thread,
      messages: thread.messages?.map((message) => ({
        ...message,
        content: getMessageText(message)
      }))
    }));

    const fuse = new Fuse(threadsWithTextMessages, options);
    searchResults = fuse.search(searchText);
    filteredThreads = searchResults.map((result) => result.item);
  }
</script>

<!--Custom styling allows center SidebarGroup (chat threads) to scroll-->
<Sidebar
  data-testid="sidebar"
  class="sidebar-height flex w-[var(--sidebar-width)] border-r border-gray-700  dark:bg-gray-800 "
>
  <SidebarWrapper class="flex w-full flex-col p-0">
    <SidebarGroup>
      <div class="flex flex-col gap-2 px-3 py-4">
        <Button on:click={() => threadsStore.changeThread('')} class="justify-between">
          New chat <PlusOutline />
        </Button>
        <Input type="txt" placeholder="Search..." bind:value={searchText} maxlength={25}></Input>
      </div>
    </SidebarGroup>
    <Hr classHr="my-0" />
    <SidebarGroup class="no-scrollbar flex-grow overflow-y-scroll px-3" data-testid="threads">
      {#each organizedThreads as category}
        {#if category.threads.length > 0}
          <SidebarDropdownWrapper
            label={category.label}
            isOpen={true}
            spanClass="flex-1 text-left whitespace-nowrap"
            ulClass="pt-0.5 pb-1 space-y-2"
          >
            {#each category.threads as thread (thread.id)}
              <LFSidebarDropdownItem
                threadId={thread.id}
                label={thread.metadata.label}
                active={activeThreadId === thread.id}
                labelClass="ps-4"
              />
            {/each}
          </SidebarDropdownWrapper>
        {/if}
      {/each}
    </SidebarGroup>
    <Hr classHr="my-0" />
    <SidebarGroup class="px-3 py-4">
      <ImportExport />
    </SidebarGroup>
  </SidebarWrapper>
</Sidebar>
