<script lang="ts">
  import { goto } from '$app/navigation';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import AssistantCard from '$components/AssistantCard.svelte';
  import type { LFAssistant } from '$lib/types/assistants';
  import { Button, Heading, TableSearch } from 'flowbite-svelte';
  import { PlusOutline } from 'flowbite-svelte-icons';
  import { assistantsStore } from '$stores';

  let searchText = '';
  let searchResults: FuseResult<LFAssistant>[];
  let filteredAssistants: LFAssistant[] = [];
  $: assistantsToDisplay = searchText ? filteredAssistants : $assistantsStore.assistants;

  const options: IFuseOptions<unknown> = {
    keys: ['name', 'description', 'instructions'],
    minMatchCharLength: 3,
    shouldSort: false,
    findAllMatches: true,
    threshold: 0, // perfect matches only
    ignoreLocation: true
  };

  $: if (searchText) {
    const fuse = new Fuse($assistantsStore.assistants, options);
    searchResults = fuse.search(searchText);
    filteredAssistants = searchResults.map((result) => result.item);
  }
</script>

<div class="no-scrollbar flex w-3/4 flex-col gap-4 overflow-y-scroll py-2">
  <Heading tag="h3" class="mb-4">Assistants Management</Heading>

  <div class="flex items-center justify-between">
    <TableSearch
      placeholder="Search"
      hoverable={true}
      bind:inputValue={searchText}
      innerDivClass="px-0"
    />

    <Button on:click={() => goto('/chat/assistants-management/new')} class="h-11"
      ><PlusOutline class="me-2 h-5 w-5" />New assistant</Button
    >
  </div>

  <div
    data-testid="assistants grid"
    class="no-scrollbar grid grid-cols-3 gap-8 overflow-y-auto 3xl:grid-cols-6"
  >
    {#each assistantsToDisplay as assistant (assistant.id)}
      <AssistantCard {assistant} />
    {/each}
  </div>
</div>
