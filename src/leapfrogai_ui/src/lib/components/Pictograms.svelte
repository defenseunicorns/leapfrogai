<script lang="ts">
  import { ClickableTile, Search } from 'carbon-components-svelte';
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
</script>

<div class="pictogram-container">
  <div style="width:22rem" class="search">
    <Search placeholder="Search" expanded size="sm" bind:value={searchText} />
  </div>
  <div class="gallery" style="height: 100%">
    {#each filteredPictograms.length > 0 ? filteredPictograms : pictogramNames as pictogram, index}
      <div class="pictogram" class:clicked={index === clickedIndex}>
        <ClickableTile on:click={(e) => handlePictogramClick(e, index, pictogram)}>
          <DynamicPictogram iconName={pictogram} />
        </ClickableTile>
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
