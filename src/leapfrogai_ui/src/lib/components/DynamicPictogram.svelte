<script lang="ts">
  import { iconMap } from '$lib/constants/iconMap';

  export let iconName: string;
  export let width = '40px';
  export let height = '40px';

  let Pictogram = iconMap.default;

  $: {
    // Avoids a complex type union error
    if (iconName in iconMap) {
      Pictogram = iconMap[iconName as keyof typeof iconMap];
    }
  }
</script>

<svelte:component this={Pictogram} {width} {height} />
