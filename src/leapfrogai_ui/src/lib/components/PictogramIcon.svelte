<script lang="ts">
  import { iconMap } from '$lib/constants/iconMap';

  export let iconName: string;

  $: Pictogram = iconMap[iconName as keyof typeof iconMap] || iconMap.default;
</script>


<svelte:component this={Pictogram} />
