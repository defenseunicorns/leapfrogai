<script lang="ts">
  import { P, Toast } from 'flowbite-svelte';
  import type { ToastNotificationProps } from '$lib/types/toast';
  import { getColor, getIconComponent } from '$helpers/toastHelpers';

  export let toast: ToastNotificationProps;

  let { title, subtitle, kind } = toast;

  $: color = getColor(kind);
</script>

<Toast {color} contentClass="w-full text-sm font-normal truncate">
  <svelte:fragment slot="icon">
    <svelte:component this={getIconComponent(kind)} class="h-5 w-5" />
    <span class="sr-only">Toast icon</span>
  </svelte:fragment>
  <div class="flex flex-col truncate">
    {title}
    {#if subtitle}
      <P size="xs" class="truncate">{subtitle}</P>
    {/if}
    <P size="xs">{`Time stamp [${new Date().toLocaleTimeString()}]`}</P>
  </div>
</Toast>
