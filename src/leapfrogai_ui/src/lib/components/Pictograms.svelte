<script lang="ts">
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import { iconMap } from '$lib/constants/iconMap';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { TableSearch } from 'flowbite-svelte';
  import { twMerge } from 'tailwind-merge';

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

<div class="flex flex-col gap-4">
  <TableSearch
    placeholder="Search"
    hoverable={true}
    bind:inputValue={searchText}
    innerDivClass="px-0"
  />

  <div class="flex flex-wrap overflow-y-scroll gap-4 justify-center">
    {#each filteredPictograms.length > 0 ? filteredPictograms : pictogramNames as pictogram}
      <button
        class="remove-btn-style transition-fill duration-70 flex cursor-pointer items-center justify-center ease-in hover:bg-gray-700"
        on:click|preventDefault={() => (selectedPictogramName = pictogram)}
        use:scrollToPictogram={{ active: pictogram === selectedPictogramName }}
      >
        <DynamicPictogram
          iconName={pictogram}
          size="lg"
          class={pictogram === selectedPictogramName && 'border-2 border-white'}
        />
      </button>
    {/each}
  </div>
  <input type="hidden" name="pictogram" value={selectedPictogramName} />
</div>
