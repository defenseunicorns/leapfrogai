<script lang="ts">
  import { goto } from '$app/navigation';
  import { fade } from 'svelte/transition';
  import { Button, ClickableTile, Search } from 'carbon-components-svelte';
  import { Add, User } from 'carbon-icons-svelte';
  import { onMount } from 'svelte';
  import { assistantsStore } from '$stores';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';

  export let data;

  let searchText = '';
  let searchResults: FuseResult<Assistant>[];
  let filteredAssistants: Assistant[] = [];
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

  onMount(() => {
    assistantsStore.setAssistants(data.assistants);
  });
</script>

<div class="container">
  <div class="inner-container">
    <div class="title">Assistants Management</div>

    <div class="utils">
      <div style="width: 20.5rem">
        <Search
          placeholder="Search"
          expanded
          size="sm"
          style="width: 20.5rem"
          bind:value={searchText}
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
        <div class="assistant-card" transition:fade={{ duration: 70 }}>
          <ClickableTile>
            <User width="40px" height="40px" />
            <div class="name">{assistant.name}</div>
            <!--There isn't a simple solution for multi line text ellipses, so doing it manually at specific character length instead-->
            <div class="description">
              {assistant.description && assistant.description.length > 73
                ? `${assistant.description?.slice(0, 73)}...`
                : assistant.description}
            </div>
          </ClickableTile>
        </div>
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

  .title {
    @include type.type-style('heading-05');
  }

  .name {
    @include type.type-style('heading-03');
  }
  .description {
    @include type.type-style('body-01');
  }

  .assistants-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: layout.$spacing-07;
    overflow-y: auto;
  }
  .assistant-card {
    :global(.bx--tile) {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: layout.$spacing-05;
      padding: 1rem;
      width: 288px;
      height: 172px;
      overflow: hidden;
    }
  }
</style>
