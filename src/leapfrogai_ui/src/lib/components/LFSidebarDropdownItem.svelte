<!--
This is a modified version of Flowbite Svelte's SidebarDropdownItem.svelte component
It adds a "three-dot" menu button with Dropdown, and delete confirmation Modal
-->
<script lang="ts">
  import { twMerge } from 'tailwind-merge';
  import { Button, Dropdown, DropdownItem, Input, Modal, P } from 'flowbite-svelte';
  import { DotsVerticalOutline, ExclamationCircleOutline } from 'flowbite-svelte-icons';
  import { threadsStore } from '$stores';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { MAX_LABEL_SIZE } from '$constants';

  export let sClass: string =
    'flex items-center p-2 ps-4 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700';
  export let threadId: string;
  export let label: string = '';
  export let activeClass: string =
    'flex items-center p-2 ps-4 text-base font-normal text-gray-900 bg-gray-200 dark:bg-gray-700 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700';
  export let active: boolean = false;
  export let labelClass: string = '';
  let deleteModalOpen = false;
  let editLabelText: string | undefined = label;
  let editLabelInputDisabled = false;
  let hovered = false;

  $: popperOpen = false;
  $: editMode = false;

  const handleEditClick = (e) => {
    e.preventDefault();
    editMode = true;
    popperOpen = false;
  };

  const resetEditMode = () => {
    editLabelText = undefined;
    editLabelInputDisabled = false;
    editMode = false;
  };

  const saveNewLabel = async () => {
    if (editLabelText) {
      editLabelInputDisabled = true;
      await threadsStore.updateThreadLabel(threadId, editLabelText);
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
    resetEditMode();
    deleteModalOpen = false;
    await threadsStore.deleteThread(threadId);
    if (threadId === $page.params.thread_id) await goto('/chat');
  };
</script>

<li
  class="flex flex-grow justify-between"
  on:mouseover={() => (hovered = true)}
  on:mouseout={() => (hovered = false)}
  on:focus
  on:blur
>
  {#if editMode}
    <Input
      data-testid="edit-thread-input"
      bind:value={editLabelText}
      type="text"
      size="sm"
      on:blur={(e) => {
        e.stopPropagation();
        handleEdit(e);
      }}
      disabled={editLabelInputDisabled}
      autofocus
      on:keydown={(e) => {
        e.stopPropagation();
        handleEdit(e);
      }}
      on:click={(e) => {
        e.stopPropagation();
      }}
      on:focus={() => {}}
      maxlength={MAX_LABEL_SIZE}
    />
  {:else}
    <button
      {...$$restProps}
      on:blur
      on:focus
      on:keydown
      on:keypress
      on:keyup
      on:mouseenter
      on:mouseleave
      on:mouseover
      on:click={async () => {
        await threadsStore.changeThread(threadId);
      }}
      aria-label={label}
      class={twMerge(
        active ? activeClass : sClass,
        'truncate',
        'flex-grow',
        'cursor-pointer',
        'justify-between',
        $$props.class
      )}
    >
      <P size="sm" class={twMerge('truncate whitespace-nowrap', labelClass)}>
        {label}
      </P>
      <button
        data-testid={`thread-menu-btn-${label}`}
        id={`btn-${threadId}`}
        class={!hovered && 'opacity-0'}
        on:click={(e) => {
          e.stopPropagation();
        }}
      >
        <DotsVerticalOutline class="dark:text-gray-400 dark:hover:text-white" />
      </button>
    </button>

    <Dropdown
      data-testid={'sidebar-popover'}
      placement="right"
      trigger="click"
      triggeredBy={`#btn-${threadId}`}
      on:show={() => {
        popperOpen = !popperOpen;
      }}
    >
      <DropdownItem on:click={handleEditClick}>Edit</DropdownItem>
      <DropdownItem
        on:click={(e) => {
          e.stopPropagation();
          deleteModalOpen = true;
        }}>Delete</DropdownItem
      >
    </Dropdown>
  {/if}
</li>

<Modal
  data-testid="delete-thread-modal"
  bind:open={deleteModalOpen}
  autoclose
  title="Delete Chat"
  color="primary"
>
  <div class="flex flex-col gap-4">
    <ExclamationCircleOutline class="mx-auto  h-12 w-12 text-gray-400 dark:text-white" />
    <P size="xl" class={twMerge('text-center dark:text-gray-400', labelClass)}>
      Are you sure you want to delete your <strong>{label.substring(0, MAX_LABEL_SIZE)}</strong> chat?
    </P>
    <div class="flex justify-end gap-2">
      <Button color="alternative" size="sm">Cancel</Button>
      <Button color="red" on:click={handleDelete} size="sm">Delete</Button>
    </div>
  </div>
</Modal>
