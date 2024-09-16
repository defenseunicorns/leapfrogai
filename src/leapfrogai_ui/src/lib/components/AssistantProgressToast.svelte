<!--
Note - fully testing the assistant progress toast has proven difficult with Playwright. Sometimes the websocket
 connection for the Supabase realtime listeners works, and sometimes it does not. Due to the dynamic nature of
 how this component updates in realtime, unit testing is limited.
 There is an issue in the backlog to re-address at some point:
 TODO - https://github.com/defenseunicorns/leapfrogai/issues/981
 -->

<script lang="ts">
  import { P, Toast } from 'flowbite-svelte';
  import type { ToastKind, ToastNotificationProps } from '$lib/types/toast';
  import AssistantProgressToastContent from '$components/AssistantProgressToastContent.svelte';
  import { getColor, getIconComponent } from '$helpers/toastHelpers';
  import { onMount } from 'svelte';
  import { toastStore } from '$stores';
  import { FILE_VECTOR_TIMEOUT_MSG_TOAST } from '$constants/toastMessages';

  export let toast: ToastNotificationProps;
  // Processing timeout
  export let timeout: number = 5 * 60 * 1000;

  let { id, subtitle, kind } = toast;
  let timeoutId: number;

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
  // If the files are still processing after x minutes, dismiss the toast and
  // pop a new error toast
  onMount(() => {
    timeoutId = setTimeout(() => {
      toastStore.addToast(FILE_VECTOR_TIMEOUT_MSG_TOAST());
      toastStore.dismissToast(id);
    }, timeout);
    return () => {
      clearTimeout(timeoutId);
    };
  });
</script>

<Toast
  {color}
  align={false}
  data-testid="assistant-progress-toast"
  contentClass="w-full text-sm font-normal truncate"
>
  <svelte:fragment slot="icon">
    <svelte:component this={getIconComponent(kind)} class="h-5 w-5" />
    <span class="sr-only">Toast icon</span>
  </svelte:fragment>
  <div class="flex flex-col truncate">
    {getAssistantVariantTitle(kind)}
    {#if subtitle}
      <P size="xs" class="truncate">{subtitle}</P>
    {/if}

    <AssistantProgressToastContent
      toastId={id}
      fileIds={toast.fileIds}
      vectorStoreId={toast.vectorStoreId}
      on:statusChange={(e) => {
        kind = e.detail;
      }}
    />

    <P size="xs">{`Time stamp [${new Date().toLocaleTimeString()}]`}</P>
  </div>
</Toast>
