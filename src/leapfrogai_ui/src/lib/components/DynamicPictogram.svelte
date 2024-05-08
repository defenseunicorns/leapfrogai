<script lang="ts">
  import { iconMap } from '$lib/constants/iconMap';

  export let iconName: string;

  let Pictogram = iconMap.default;

  $: {
    // Avoids a complex type union error
    if (iconName in iconMap) {
      Pictogram = iconMap[iconName as keyof typeof iconMap];
    }
  }
</script>

<svelte:component this={Pictogram} width="40px" height="40px"/>
