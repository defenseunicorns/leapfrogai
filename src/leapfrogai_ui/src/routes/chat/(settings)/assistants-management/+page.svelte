<script lang="ts">
  import { goto } from '$app/navigation';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import AssistantTile from '$components/AssistantTile.svelte';
  import type { LFAssistant } from '$lib/types/assistants';
  import { Button, Heading, TableSearch } from 'flowbite-svelte';
  import { PlusOutline } from 'flowbite-svelte-icons';

  export let data;

  let searchText = '';
  let searchResults: FuseResult<LFAssistant>[];
  let filteredAssistants: LFAssistant[] = [];
  $: assistantsToDisplay = searchText ? filteredAssistants : data.assistants;

  const options: IFuseOptions<unknown> = {
    keys: ['name', 'description', 'instructions'],
    minMatchCharLength: 3,
    shouldSort: false,
    findAllMatches: true,
    threshold: 0, // perfect matches only
    ignoreLocation: true
  };

  $: if (searchText) {
    const fuse = new Fuse(data.assistants, options);
    searchResults = fuse.search(searchText);
    filteredAssistants = searchResults.map((result) => result.item);
  }
</script>

<div class="flex flex-col gap-4 px-48 py-2">
  <Heading tag="h3">Assistants Management</Heading>

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
  <div data-testid="assistants grid" class="grid grid-cols-3 gap-8 overflow-y-auto">
    {#each assistantsToDisplay as assistant (assistant.id)}
      <AssistantTile {assistant} />
    {/each}
  </div>
</div>
