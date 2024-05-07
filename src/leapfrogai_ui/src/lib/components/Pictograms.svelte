<script lang="ts">
  import { onMount, type SvelteComponent } from 'svelte';
  import { ClickableTile, Search } from 'carbon-components-svelte';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';

  type Pictogram = {
    name: string;
    Component: typeof SvelteComponent;
  };

  export let selectedPictogramName: string;

  let pictograms: Pictogram[] = [];
  let filteredPictograms: Pictogram[] = [];
  let searchText = '';
  let searchResults: FuseResult<Pictogram>[];

  let clickedIndex: number;

  const options: IFuseOptions<unknown> = {
    keys: ['name'],
    minMatchCharLength: 3,
    shouldSort: false,
    findAllMatches: true,
    threshold: 0, // perfect matches only
    ignoreLocation: true
  };

  $: if (searchText) {
    const fuse = new Fuse(pictograms, options);
    searchResults = fuse.search(searchText);
    filteredPictograms = searchResults.map((result) => result.item);
  }

  const handlePictogramClick = (e: MouseEvent, index: number, name: string) => {
    clickedIndex = index;
    selectedPictogramName = name;
  };

  // Dynamically importing pictograms for performance
  onMount(async () => {
    const module = await import('carbon-pictograms-svelte');
    pictograms = Object.entries(module).map(([name, component]) => ({
      name,
      Component: component as typeof SvelteComponent
    }));
  });
</script>

<div class="pictogram-container">
  <div style="width:22rem" class="search">
    <Search placeholder="Search" expanded size="sm" bind:value={searchText} />
  </div>
  <div class="gallery" style="height: 100%">
    {#each filteredPictograms.length > 0 ? filteredPictograms : pictograms as { Component }, index}
      <div class="pictogram" class:clicked={index === clickedIndex}>
        <ClickableTile on:click={(e) => handlePictogramClick(e, index, Component.name)}>
          <svelte:component this={Component} /></ClickableTile
        >
      </div>
    {/each}
  </div>
  <input type="hidden" name="pictogram" value={selectedPictogramName} />
</div>

<style lang="scss">
  .pictogram-container {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-05;
  }
  .search {
    :global(.bx--search-input) {
      background-color: themes.$layer-01;
    }
  }
  .gallery {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
  }

  .pictogram {
    box-sizing: border-box; // width and height must be specified for border-box
    width: 132px;
    height: 104px;
    text-align: center;
  }
  .clicked {
    border: 2px solid white;
  }
</style>
