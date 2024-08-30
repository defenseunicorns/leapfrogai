<script lang="ts">
  import { P, Toast } from 'flowbite-svelte';
  import {
    BanOutline,
    CheckCircleSolid,
    ExclamationCircleOutline,
    InfoCircleOutline
  } from 'flowbite-svelte-icons';
  import type { ToastKind, ToastNotificationProps } from '$lib/types/toast';
  import AssistantProgressToastContent from '$components/AssistantProgressToastContent.svelte';
  import ToastOverride from '$components/ToastOverride.svelte';

  export let toast: ToastNotificationProps;

  let { id, title, subtitle, kind, variant } = toast;

  $: color = getColor(kind);
  $: IconComponent = getIconComponent(kind);

  function getColor(toastKind: ToastKind) {
    switch (toastKind) {
      case 'success':
        return 'green';
      case 'info':
        return 'blue';
      case 'warning':
        return 'yellow';
      case 'error':
        return 'red';
      default:
        return 'blue';
    }
  }

  function getIconComponent(toastKind: ToastKind) {
    switch (toastKind) {
      case 'success':
        return CheckCircleSolid;
      case 'info':
        return InfoCircleOutline;
      case 'warning':
        return ExclamationCircleOutline;
      case 'error':
        return BanOutline;
      default:
        return InfoCircleOutline;
    }
  }

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
    {variant === 'assistant-progress' ? getAssistantVariantTitle(kind) : title}
    {#if subtitle}
      <P size="xs">{subtitle}</P>
    {/if}
    {#if variant === 'assistant-progress'}
      <AssistantProgressToastContent
        toastId={id}
        fileIds={toast.fileIds}
        vectorStoreId={toast.vectorStoreId}
        on:statusChange={(e) => {
          kind = e.detail;
        }}
      />
    {/if}
    <P size="xs">{`Time stamp [${new Date().toLocaleTimeString()}]`}</P>
  </div>
</ToastOverride>
