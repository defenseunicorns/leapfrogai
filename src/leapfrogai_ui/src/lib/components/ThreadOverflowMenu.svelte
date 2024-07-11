<script lang="ts">
  import { OverflowMenu, OverflowMenuItem } from 'carbon-components-svelte';
  import type { LFThread } from '$lib/types/threads';
  import { uiStore } from '$stores';

  export let thread: LFThread;
  export let scrollOffset = 0;
  export let editLabelText: string | undefined = undefined;
  export let parentSideNavRef: HTMLAnchorElement;
  export let editMode: boolean;
  export let deleteModalOpen: boolean;

  let isOpen: boolean;
  let buttonRef: HTMLButtonElement;

  $: positioningHeight = Math.abs((parentSideNavRef?.offsetTop || 0) - scrollOffset + 48);
</script>

<OverflowMenu
  id={`overflow-menu-${thread.id}`}
  bind:buttonRef
  bind:open={isOpen}
  data-testid="overflow-menu-{thread.metadata.label}"
  style={isOpen
    ? `position: fixed; top: 0; left: 0; transform: translate(224px, ${positioningHeight}px)`
    : ''}
  on:click={(e) => {
    e.stopPropagation();
    uiStore.setSelectedThreadOverflowMenuId(thread.id);
  }}
>
  <OverflowMenuItem
    text="Edit"
    on:click={(e) => {
      e.stopPropagation();
      editLabelText = thread.metadata.label;
      editMode = true;
    }}
  />

  <OverflowMenuItem
    data-testid="overflow-menu-delete-{thread.metadata.label}"
    text="Delete"
    on:click={(e) => {
      e.stopPropagation();
      deleteModalOpen = true;
    }}
  />
</OverflowMenu>
