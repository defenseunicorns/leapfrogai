<script lang="ts">
  import { Search } from 'carbon-components-svelte';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import { iconMap } from '$lib/constants/iconMap';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';

  export let selectedPictogramName: string;

  let filteredPictograms: (keyof typeof iconMap)[] = [];
  let searchText = '';
  let searchResults: FuseResult<(keyof typeof iconMap)[]>[];

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

  const resetSearch = () => {
    searchText = '';
    filteredPictograms = [];
  };

  function scrollToPictogram(node: HTMLElement, params: { active: boolean }) {
    if (params.active) {
      node.scrollIntoView({ behavior: 'auto', block: 'nearest' });
    }
    return {
      update(newParams: { active: boolean }) {
        if (newParams.active) {
          node.scrollIntoView({ behavior: 'auto', block: 'nearest' });
        }
      }
    };
  }
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
    {#each filteredPictograms.length > 0 ? filteredPictograms : pictogramNames as pictogram}
      <button
        class="pictogram remove-btn-style"
        class:clicked={pictogram === selectedPictogramName}
        on:click|preventDefault={() => (selectedPictogramName = pictogram)}
        use:scrollToPictogram={{ active: pictogram === selectedPictogramName }}
      >
        <DynamicPictogram iconName={pictogram} width="64px" height="64px" />
      </button>
    {/each}
  </div>
  <input type="hidden" name="pictogram" value={selectedPictogramName} />
</div>

<style lang="scss">
  .pictogram-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    height: 100%;
  }
  .search {
    :global(.bx--search-input) {
      background-color: #393939;
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
      background-color: #474747;
    }
  }
  .clicked {
    border: 2px solid white;
  }
</style>
