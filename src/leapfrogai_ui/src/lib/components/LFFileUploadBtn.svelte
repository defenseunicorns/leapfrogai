<script lang="ts">
  import { twMerge } from 'tailwind-merge';
  import { Button } from 'flowbite-svelte';

  export let files: FileList | undefined = undefined;
  export let ref: HTMLInputElement | null = null;
  export let accept: string[] = [];
  export let multiple = false;
  export let disabled = false;
  export let size: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'none' = 'sm';
</script>

<input
  bind:this={ref}
  type="file"
  accept={accept.join(',')}
  {multiple}
  on:keydown={({ key }) => {
    if (key === ' ' || key === 'Enter') {
      ref?.click();
    }
  }}
  bind:files
  on:change
  class="sr-only"
  {...$$restProps}
/>
<Button
  outline
  {size}
  {disabled}
  on:click={() => ref?.click()}
  class={twMerge('w-full', $$props.class)}
>
  <div class="flex w-full justify-between">
    <slot />
  </div>
</Button>
