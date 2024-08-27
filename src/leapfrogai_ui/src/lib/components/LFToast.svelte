<script lang="ts">
  import { P, Toast } from 'flowbite-svelte';
  import {
    BanOutline,
    CheckCircleSolid,
    ExclamationCircleOutline,
    InfoCircleOutline
  } from 'flowbite-svelte-icons';

  export let toast: ToastNotificationProps;

  let { title, subtitle, kind } = toast;

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
</script>

<Toast {color}>
  <svelte:fragment slot="icon">
    <IconComponent class="h-5 w-5" />
    <span class="sr-only">Check icon</span>
  </svelte:fragment>
  <div class="flex flex-col">
    {title}
    {#if subtitle}
      <P size="xs">{subtitle}</P>
    {/if}
    <P size="xs">{`Time stamp [${new Date().toLocaleTimeString()}]`}</P>
  </div>
</Toast>
