<script lang="ts">
  import { iconMap } from '$lib/constants/iconMap';
  import { twMerge } from 'tailwind-merge';

  export let iconName = 'default';
  export let size: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'none' = 'md';

  let Pictogram = iconMap.default;

  const sizes = {
    xs: 'w-6 h-6',
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-20 h-20',
    xl: 'w-36 h-36',
    none: ''
  };

  $: {
    // Avoids a complex type union error
    if (iconName in iconMap) {
      Pictogram = iconMap[iconName as keyof typeof iconMap];
    }
  }

  let pictogramClass: string;
  $: pictogramClass = twMerge(sizes[size], $$props.class);
</script>

<svelte:component this={Pictogram} class={pictogramClass} data-testid={`pictogram-${iconName}`} />
