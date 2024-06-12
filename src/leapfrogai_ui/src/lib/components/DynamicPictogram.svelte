<script lang="ts">
  import { iconMap } from '$lib/constants/iconMap';

  export let iconName = 'default';
  export let width = '40px';
  export let height = '2.5rem';

  let Pictogram = iconMap.default;

  $: {
    // Avoids a complex type union error
    if (iconName in iconMap) {
      Pictogram = iconMap[iconName as keyof typeof iconMap];
    }
  }
</script>

<svelte:component this={Pictogram} {width} {height} data-testid={`pictogram-${iconName}`} />
