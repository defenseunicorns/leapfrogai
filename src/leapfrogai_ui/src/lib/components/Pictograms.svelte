<script lang="ts">
  import { Search } from 'carbon-components-svelte';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import { iconMap } from '$lib/constants/iconMap';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';

  export let selectedPictogramName: string;

  let filteredPictograms: (keyof typeof iconMap)[] = [];
  let searchText = '';
  let searchResults: FuseResult<(keyof typeof iconMap)[]>[];
  let clickedIndex: number;

  const pictogramNames = Object.keys(iconMap);

  const options: IFuseOptions<unknown> = {
    minMatchCharLength: 3,
    shouldSort: false,
    findAllMatches: true,
    threshold: 0, // perfect matches only
    ignoreLocation: true
  };

  $: if (searchText) {
    const fuse = new Fuse(pictogramNames, options);
    searchResults = fuse.search(searchText);
    filteredPictograms = searchResults.map(
      (result) => result.item
    ) as unknown as (keyof typeof iconMap)[];
  }

  const handlePictogramClick = (e: MouseEvent, index: number, name: string) => {
    clickedIndex = index;
    selectedPictogramName = name;
  };

  const resetSearch = () => {
    searchText = '';
    filteredPictograms = [];
  };
</script>

<div class="pictogram-container">
  <div style="width:22rem" class="search">
    <Search
      placeholder="Search"
      expanded
      size="sm"
      bind:value={searchText}
      on:clear={resetSearch}
    />
  </div>
  <div class="gallery">
    {#each filteredPictograms.length > 0 ? filteredPictograms : pictogramNames as pictogram, index}
      <div
        class="pictogram"
        class:clicked={index === clickedIndex}
        on:click={(e) => handlePictogramClick(e, index, pictogram)}
      >
        <DynamicPictogram iconName={pictogram} width="64px" height="64px" />
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
    height: 100%;
  }
  .search {
    :global(.bx--search-input) {
      background-color: themes.$layer-01;
    }
  }
  .gallery {
    display: flex;
    flex-wrap: wrap;
    overflow-y: scroll;
    scrollbar-width: none;
  }

  .pictogram {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 112px;
    height: 112px;
    padding: 16px;
    cursor: pointer;
    transition: fill 70ms ease;
    &:hover {
      background-color: themes.$layer-hover-01;
    }
  }
  .clicked {
    border: 2px solid white;
  }
</style>
