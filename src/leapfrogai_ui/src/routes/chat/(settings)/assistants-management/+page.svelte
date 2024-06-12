<script lang="ts">
  import { goto } from '$app/navigation';
  import { Button, Search } from 'carbon-components-svelte';
  import { Add } from 'carbon-icons-svelte';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import AssistantTile from '$components/AssistantTile.svelte';
  import type { LFAssistant } from '$lib/types/assistants';

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
  const resetSearch = () => {
    searchText = '';
    filteredAssistants = [];
  };
</script>

<div class="container">
  <div class="inner-container">
    <div class="preview-banner">
      Assistants Management is a preview only. It is not yet fully functional.
    </div>
    <div class="title">Assistants Management</div>

    <div class="utils">
      <div style="width: 20.5rem">
        <Search
          placeholder="Search"
          expanded
          size="sm"
          style="width: 20.5rem"
          bind:value={searchText}
          on:clear={resetSearch}
        />
      </div>
      <Button
        kind="primary"
        size="small"
        icon={Add}
        on:click={() => goto('/chat/assistants-management/new')}>New assistant</Button
      >
    </div>
    <div data-testid="assistants grid" class="assistants-grid">
      {#each assistantsToDisplay as assistant (assistant.id)}
        <AssistantTile {assistant} />
      {/each}
    </div>
  </div>
</div>

<style lang="scss">
  .container {
    display: flex;
    justify-content: center;
    max-height: 90%;
  }
  .inner-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    width: 943px; // 3 tiles, plus gap, plus scrollbar
  }

  .utils {
    display: flex;
    justify-content: space-between;
  }

  .assistants-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: layout.$spacing-07;
    overflow-y: auto;
  }

  .title {
    @include type.type-style('heading-05');
  }

  .preview-banner {
    text-align: center;
    color: $red-30;
  }
</style>
