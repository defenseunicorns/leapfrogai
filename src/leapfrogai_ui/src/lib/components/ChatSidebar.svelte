<script lang="ts">
  import {
    Button,
    Modal,
    OverflowMenu,
    OverflowMenuItem,
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
  import { browser } from '$app/environment';
  import ImportExport from '$components/ImportExport.svelte';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import { onMount } from 'svelte';
  import type { LFThread } from '$lib/types/threads';
  import { getMessageText } from '$helpers/threads';
  import { goto } from '$app/navigation';

  let deleteModalOpen = false;
  let editMode = false;
  let editThreadId: string | null = null;
  let editLabelText: string | undefined = undefined;
  let editLabelInputDisabled = false;
  let disableScroll = false;
  let overflowMenuOpen = false;
  let menuOffset = 0;
  let scrollOffset = 0;
  let activeThreadRef: HTMLElement | null;
  let scrollBoxRef: HTMLElement;
  let searchText = '';
  let searchResults: FuseResult<LFThread>[];
  let filteredThreads: LFThread[] = [];

  $: activeThread = $threadsStore.threads.find((thread) => thread.id === $page.params.thread_id);

  $: editMode = !!activeThread?.id && editThreadId === activeThread.id;

  $: organizedThreads = dates.organizeThreadsByDate(
    searchText !== '' ? filteredThreads : $threadsStore.threads
  );

  const resetEditMode = () => {
    disableScroll = false;
    editThreadId = null;
    editLabelText = undefined;
    editLabelInputDisabled = false;
  };

  const saveNewLabel = async () => {
    if (editThreadId && editLabelText) {
      editLabelInputDisabled = true;
      await threadsStore.updateThreadLabel(editThreadId, editLabelText);
      resetEditMode();
    }
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
    deleteModalOpen = false;
    if (activeThread?.id) {
      await threadsStore.deleteThread(activeThread.id);
    }
    await goto('/chat');
  };

  const handleActiveThreadChange = (id: string) => {
    threadsStore.changeThread(id);
    activeThreadRef = document.getElementById(`side-nav-menu-item-${id}`);
  };

  // To properly display the overflow menu items for each thread, we have to calculate the height they
  // should be displayed at due to the carbon override for allowing overflow
  $: if (browser && activeThreadRef) {
    menuOffset = activeThreadRef?.offsetTop;
    scrollOffset = scrollBoxRef?.scrollTop;
  } else {
    if (!activeThreadRef) {
      menuOffset = 0;
      scrollOffset = 0;
    }
  }

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
              class:noScroll={disableScroll || editMode}
              bind:this={scrollBoxRef}
              class="threads"
              data-testid="threads"
            >
              {#each organizedThreads as category}
                {#if category.threads.length > 0}
                  <SideNavMenu text={category.label} expanded data-testid="side-nav-menu">
                    {#each category.threads as thread (thread.id)}
                      <SideNavMenuItem
                        data-testid="side-nav-menu-item-{thread.metadata.label}"
                        id="side-nav-menu-item-{thread.id}"
                        isSelected={activeThread?.id === thread.id}
                        on:click={() => handleActiveThreadChange(thread.id)}
                      >
                        <div class="menu-content">
                          {#if editMode && activeThread?.id === thread.id}
                            <TextInput
                              bind:value={editLabelText}
                              size="sm"
                              class="edit-thread"
                              on:keydown={(e) => handleEdit(e)}
                              on:blur={(e) => {
                                handleEdit(e);
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
                              <OverflowMenu
                                id={`overflow-menu-${thread.id}`}
                                on:close={() => {
                                  overflowMenuOpen = false;
                                  disableScroll = false;
                                }}
                                on:click={(e) => {
                                  e.stopPropagation();
                                  overflowMenuOpen = true;
                                  handleActiveThreadChange(thread.id);
                                  disableScroll = true;
                                }}
                                data-testid="overflow-menu-{thread.metadata.label}"
                                style={overflowMenuOpen && activeThread?.id === thread.id
                                  ? `position: fixed; top: 0; left: 0; transform: translate(224px, ${menuOffset - scrollOffset + 48}px)`
                                  : ''}
                              >
                                <OverflowMenuItem
                                  text="Edit"
                                  on:click={() => {
                                    editThreadId = thread.id;
                                    editLabelText = thread.metadata.label;
                                  }}
                                />

                                <OverflowMenuItem
                                  data-testid="overflow-menu-delete-{thread.metadata.label}"
                                  text="Delete"
                                  on:click={() => {
                                    deleteModalOpen = true;
                                  }}
                                />
                              </OverflowMenu>
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
      bind:open={deleteModalOpen}
      modalHeading="Delete Chat"
      primaryButtonText="Delete"
      secondaryButtonText="Cancel"
      on:click:button--secondary={() => (deleteModalOpen = false)}
      on:open
      on:close
      on:submit={handleDelete}
      >Are you sure you want to delete your <strong
        >{activeThread?.metadata.label.substring(0, MAX_LABEL_SIZE)}</strong
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
    padding: 0 0 layout.$spacing-05 0;

    :global(.bx--side-nav__divider) {
      margin: layout.$spacing-03 0 0 0;
      background-color: themes.$border-subtle-01;
    }
  }

  .new-chat-container {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-03;
    padding: layout.$spacing-05;

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
    width: 208px;

    .menu-text {
      width: 192px;
      overflow: hidden;
      text-overflow: ellipsis;
      color: themes.$text-secondary;
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
    color: themes.$text-secondary !important;
  }

  :global(.bx--side-nav__navigation) {
    background-color: themes.$layer-01 !important;
    list-style: none;
    height: calc(100vh - var(--header-height)) !important;
    color: themes.$text-secondary !important;
  }

  :global(.bx--side-nav__items) {
    text-align: center;
    overflow: visible !important;
    height: 100%;
  }

  :global(.bx--side-nav__submenu) {
    color: themes.$text-secondary !important;

    :global(svg) {
      stroke: themes.$text-secondary;
    }

    &:hover {
      background-color: #4d4d4d !important;
    }
  }

  .label-edit-mode {
    :global(.bx--side-nav__link) {
      padding: 0 layout.$spacing-05 0 layout.$spacing-07;
    }

    :global(.bx--side-nav__link[aria-current='page']) {
      background-color: themes.$layer-01 !important;
    }

    :global(input) {
      height: 1.5rem;
    }

    :global(.bx--text-input) {
      border-bottom: none;
    }
  }
</style>
