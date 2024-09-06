<script lang="ts">
  import { P } from 'flowbite-svelte';
  import type { ToastNotificationProps } from '$lib/types/toast';
  import ToastOverride from '$components/ToastOverride.svelte';
  import { getColor, getIconComponent } from '$helpers/toastHelpers';

  export let toast: ToastNotificationProps;

  let { title, subtitle, kind } = toast;

  $: color = getColor(kind);
</script>

<ToastOverride {color}>
  <svelte:fragment slot="icon">
    <svelte:component this={getIconComponent(kind)} class="h-5 w-5" />
    <span class="sr-only">Toast icon</span>
  </svelte:fragment>
  <div class="flex flex-col">
    {title}
    {#if subtitle}
      <P size="xs">{subtitle}</P>
    {/if}
    <P size="xs">{`Time stamp [${new Date().toLocaleTimeString()}]`}</P>
  </div>
</ToastOverride>
