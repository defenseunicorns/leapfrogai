<script lang="ts">
  import {
    Button,
    Modal,
    SideNav,
    SideNavItems,
    SideNavMenu,
    SideNavMenuItem,
    TextInput
  } from 'carbon-components-svelte';
  import { AddComment } from 'carbon-icons-svelte';
  import { dates } from '$helpers';
  import { MAX_LABEL_SIZE } from '$lib/constants';
  import { threadsStore, uiStore } from '$stores';
  import { page } from '$app/stores';
  import ImportExport from '$components/ImportExport.svelte';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import { onMount } from 'svelte';
  import type { LFThread } from '$lib/types/threads';
  import { getMessageText } from '$helpers/threads';
  import { goto } from '$app/navigation';
  import ThreadOverflowMenu from '$components/ThreadOverflowMenu.svelte';

  let deleteModalOpen = false;
  let editLabelInputDisabled = false;
  let scrollOffset = 0;
  let scrollBoxRef: HTMLElement;
  let searchText = '';
  let searchResults: FuseResult<LFThread>[];
  let filteredThreads: LFThread[] = [];
  let editLabelText: string | undefined;
  let sideNavItemRefs: { [id: string]: HTMLAnchorElement } = {};
  let editMode = false;

  $: activeThread = $page.data.thread;
  $: organizedThreads = dates.organizeThreadsByDate(
    searchText !== '' ? filteredThreads : $threadsStore.threads
  );
  $: selectedThread = $threadsStore.threads.find(
    (thread) => thread.id === $uiStore.selectedThreadOverflowMenuId
  );

  const resetEditMode = () => {
    uiStore.setSelectedThreadOverflowMenuId('');
    editLabelText = undefined;
    editLabelInputDisabled = false;
    editMode = false;
  };

  const saveNewLabel = async () => {
    if ($uiStore.selectedThreadOverflowMenuId && editLabelText) {
      editLabelInputDisabled = true;
      await threadsStore.updateThreadLabel($uiStore.selectedThreadOverflowMenuId, editLabelText);
    }
    resetEditMode();
  };

  const handleEdit = async (e: KeyboardEvent | FocusEvent) => {
    if (e.type === 'blur') {
      await saveNewLabel();
    }
    if (e.type === 'keydown') {
      const keyboardEvent = e as KeyboardEvent;
      if (keyboardEvent.key === 'Escape') {
        resetEditMode();
        return;
      }

      if (keyboardEvent.key === 'Enter' || keyboardEvent.key === 'Tab') {
        await saveNewLabel();
      }
    }
  };

  const handleDelete = async () => {
    delete sideNavItemRefs[$uiStore.selectedThreadOverflowMenuId];
    deleteModalOpen = false;
    if ($uiStore.selectedThreadOverflowMenuId) {
      await threadsStore.deleteThread($uiStore.selectedThreadOverflowMenuId);
    }
    await goto('/chat');
  };

  const handleActiveThreadChange = (id: string) => {
    threadsStore.changeThread(id);
  };

  const options: IFuseOptions<unknown> = {
    keys: ['metadata.label', 'messages.content'],
    minMatchCharLength: 3,
    shouldSort: false,
    findAllMatches: true,
    threshold: 0, // perfect matches only
    ignoreLocation: true
  };

  $: if (searchText) {
    // Remap the message content to be a string instead of string | nested object
    const threadsWithTextMessages = $threadsStore.threads.map((thread) => ({
      ...thread,
      messages: thread.messages?.map((message) => ({
        ...message,
        content: getMessageText(message)
      }))
    }));

    const fuse = new Fuse(threadsWithTextMessages, options);
    searchResults = fuse.search(searchText);
    filteredThreads = searchResults.map((result) => result.item);
  }

  onMount(() => {
    // When trying to set the isSideNavOpen to true when initialized as a variable
    // Header component overrides it to false so menu closes, setting to true here
    // to prevent that
    uiStore.setIsSideNavOpen(true);
  });
</script>

<SideNav
  bind:isOpen={$uiStore.isSideNavOpen}
  aria-label="side navigation"
  style="background-color: g90;"
>
  <div class="inner-side-nav-container">
    <SideNavItems>
      <div class="side-nav-items-container">
        <div style="height: 100%">
          <div class="side-nav-items-container">
            <div class="new-chat-container">
              <Button
                kind="secondary"
                size="small"
                icon={AddComment}
                class="new-chat-btn"
                id="new-chat-btn"
                aria-label="new thread"
                on:click={() => handleActiveThreadChange('')}>New Chat</Button
              >
              <TextInput
                light
                size="sm"
                placeholder="Search..."
                bind:value={searchText}
                maxlength={25}
              />
              <hr id="divider" class="divider" />
            </div>

            <div
              class:noScroll={$uiStore.selectedThreadOverflowMenuId !== '' || editMode}
              bind:this={scrollBoxRef}
              class="threads"
              data-testid="threads"
              on:scroll={() => (scrollOffset = scrollBoxRef.scrollTop)}
            >
              {#each organizedThreads as category}
                {#if category.threads.length > 0}
                  <SideNavMenu text={category.label} expanded data-testid="side-nav-menu">
                    {#each category.threads as thread (thread.id)}
                      <SideNavMenuItem
                        data-testid="side-nav-menu-item-{thread.metadata.label}"
                        id="side-nav-menu-item-{thread.id}"
                        bind:ref={sideNavItemRefs[thread.id]}
                        isSelected={activeThread?.id === thread.id}
                        on:click={() => {
                          uiStore.setSelectedThreadOverflowMenuId('');
                          handleActiveThreadChange(thread.id);
                        }}
                      >
                        <div class="menu-content">
                          {#if editMode && $uiStore.selectedThreadOverflowMenuId === thread.id}
                            <TextInput
                              bind:value={editLabelText}
                              size="sm"
                              class="edit-thread"
                              on:keydown={(e) => {
                                e.stopPropagation();
                                handleEdit(e);
                              }}
                              on:blur={(e) => {
                                e.stopPropagation();
                                handleEdit(e);
                              }}
                              on:click={(e) => {
                                e.stopPropagation();
                              }}
                              autofocus
                              maxlength={MAX_LABEL_SIZE}
                              readonly={editLabelInputDisabled}
                              aria-label="edit thread"
                            />
                          {:else}
                            <div data-testid="thread-label-{thread.id}" class="menu-text">
                              {thread.metadata.label}
                            </div>
                            <div>
                              <ThreadOverflowMenu
                                {thread}
                                {scrollOffset}
                                parentSideNavRef={sideNavItemRefs[thread.id]}
                                bind:editLabelText
                                bind:editMode
                                bind:deleteModalOpen
                              />
                            </div>
                          {/if}
                        </div>
                      </SideNavMenuItem>
                    {/each}
                  </SideNavMenu>
                {/if}
              {/each}
            </div>
            <div>
              <hr id="divider" class="divider" />
              <ImportExport />
            </div>
          </div>
        </div>
      </div></SideNavItems
    >

    <Modal
      danger
      preventCloseOnClickOutside
      bind:open={deleteModalOpen}
      modalHeading="Delete Chat"
      primaryButtonText="Delete"
      secondaryButtonText="Cancel"
      on:click:button--secondary={() => (deleteModalOpen = false)}
      on:open
      on:close
      on:submit={handleDelete}
      >Are you sure you want to delete your <strong
        >{selectedThread?.metadata.label.substring(0, MAX_LABEL_SIZE)}</strong
      > chat?</Modal
    >
  </div></SideNav
>

<!-- NOTE - Carbon Components Svelte does not yet support theming of the UI Shell components so several
properties had to be manually overridden.
https://github.com/carbon-design-system/carbon-components-svelte/issues/892
-->
<style lang="scss">
  .inner-side-nav-container {
    height: 100%;

    :global(.bx--overflow-menu) {
      width: 16px;
      height: 32px;
      z-index: 1;
    }

    :global(.bx--overflow-menu-options) {
      left: 20px !important;
    }
  }

  :global(.bx--side-nav__item) {
    list-style-type: none;
  }

  .noScroll {
    overflow-y: hidden !important;
  }

  .side-nav-items-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    :global(.bx--side-nav__divider) {
      margin: 0.5rem 0 0 0;
      background-color: #525252;
    }
  }

  .new-chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem;

    :global(button.new-chat-btn) {
      width: 100%;
    }
  }

  .menu-content {
    width: 100% !important;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .menu-text {
      width: 192px;
      overflow: hidden;
      text-overflow: ellipsis;
      color: #c6c6c6;
    }
  }

  // The following overflow: visible !important overrides allow the OverflowMenu component
  // to display correctly. There may be a better way to do this, but just realize you have
  // to override things at several levels to get results.
  // The !important is necessary for the changes to work in production builds.
  .threads {
    flex-grow: 1;
    scrollbar-width: none;
    overflow-y: auto;
  }

  :global(.bx--side-nav__navigation) {
    overflow: visible !important;

    :global(.bx--side-nav__item) {
      overflow: visible !important;
      cursor: pointer;
    }
  }

  :global(.bx--side-nav__link) {
    &:hover {
      background-color: #4d4d4d !important;
    }
  }

  :global(.bx--side-nav__link[aria-current='page']) {
    background-color: #4d4d4d !important;
  }

  :global(.bx--side-nav__link-text) {
    position: relative;
    display: flex;
    flex-grow: 1;
    justify-content: space-between;
    text-align: left;
    overflow: visible !important;
    color: #c6c6c6 !important;
  }

  :global(.bx--side-nav__navigation) {
    background-color: #393939 !important;
    list-style: none;
    height: calc(100vh - var(--header-height)) !important;
    color: #c6c6c6 !important;
  }

  :global(.bx--side-nav__items) {
    text-align: center;
    overflow: visible !important;
    height: 100%;
  }

  :global(.bx--side-nav__submenu) {
    color: #c6c6c6 !important;

    :global(svg) {
      stroke: #c6c6c6;
    }

    &:hover {
      background-color: #4d4d4d !important;
    }
  }

  .label-edit-mode {
    :global(.bx--side-nav__link) {
      padding: 0 1rem 0 2rem;
    }

    :global(.bx--side-nav__link[aria-current='page']) {
      background-color: #393939 !important;
    }

    :global(input) {
      height: 1.5rem;
    }

    :global(.bx--text-input) {
      border-bottom: none;
    }
  }
</style>
