<script lang="ts">
  import { sineIn } from 'svelte/easing';
  import { uiStore } from '$stores';
  import LFSidebar from '$components/LFSidebar.svelte';
  import LFDrawer from '$components/LFDrawer.svelte';

  let transitionParams = {
    x: -320,
    duration: 200,
    easing: sineIn
  };

  $: innerWidth = 0;

  $: innerWidth < 1024 && uiStore.setOpenSidebar(false);
</script>

<svelte:window bind:innerWidth />

{#if innerWidth < 1024}
  <LFDrawer
    transitionType="fly"
    {transitionParams}
    activateClickOutside={false}
    placement="left"
    hidden={!$uiStore.openSidebar}
    class="no-scrollbar top-header flex max-w-64 overflow-y-hidden p-0"
    backdropCustomClass="top-header"
  >
    <LFSidebar />
  </LFDrawer>
{:else}
  <LFSidebar />
{/if}
