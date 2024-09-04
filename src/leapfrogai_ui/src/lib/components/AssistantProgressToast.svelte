<script lang="ts">
  import { P } from 'flowbite-svelte';
  import type { ToastKind, ToastNotificationProps } from '$lib/types/toast';
  import AssistantProgressToastContent from '$components/AssistantProgressToastContent.svelte';
  import ToastOverride from '$components/ToastOverride.svelte';
  import { getColor, getIconComponent } from '$helpers/toastHelpers';

  export let toast: ToastNotificationProps;

  let { id, title, subtitle, kind } = toast;

  $: color = getColor(kind);

  function getAssistantVariantTitle(toastKind: ToastKind) {
    switch (toastKind) {
      case 'success':
        return 'Assistant Updated';
      case 'info':
        return 'Updating Assistant Files';
      case 'warning':
        return 'Updating Assistant Files';
      case 'error':
        return 'Error Updating Assistant';
      default:
        return 'Updating Assistant Files';
    }
  }
</script>

<ToastOverride {color} align={false}>
  <svelte:fragment slot="icon">
    <svelte:component this={getIconComponent(kind)} class="h-5 w-5" />
    <span class="sr-only">Toast icon</span>
  </svelte:fragment>
  <div class="flex flex-col">
    {title}
    {#if subtitle}
      <P size="xs">{subtitle}</P>
    {/if}

    <AssistantProgressToastContent
      toastId={id}
      fileIds={toast.fileIds}
      vectorStoreId={toast.vectorStoreId}
      on:statusChange={(e) => {
        kind = e.detail;
        title = getAssistantVariantTitle(e.detail);
      }}
    />

    <P size="xs">{`Time stamp [${new Date().toLocaleTimeString()}]`}</P>
  </div>
</ToastOverride>
