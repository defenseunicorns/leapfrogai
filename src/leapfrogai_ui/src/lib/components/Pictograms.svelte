<script lang="ts">
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { iconMap } from '$constants/iconMap';
  import { twMerge } from 'tailwind-merge';

  export let pictograms: (keyof typeof iconMap)[];
  export let selectedPictogramName: string;

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

<div>
  <div class="flex flex-wrap justify-center gap-4">
    {#each pictograms as pictogram}
      <button
        class="remove-btn-style transition-fill duration-70 flex cursor-pointer items-center justify-center ease-in hover:bg-gray-700"
        on:click|preventDefault={() => (selectedPictogramName = pictogram)}
        use:scrollToPictogram={{ active: pictogram === selectedPictogramName }}
      >
        <DynamicPictogram
          iconName={pictogram}
          size="lg"
          class={twMerge(
            'text-gray-400',
            pictogram === selectedPictogramName && 'border-2 border-white '
          )}
        />
      </button>
    {/each}
  </div>

  <input type="hidden" name="pictogram" value={selectedPictogramName} />
</div>
