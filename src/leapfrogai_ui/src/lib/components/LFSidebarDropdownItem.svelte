<!--
This is a modified version of Flowbite Svelte's SidebarDropdownItem.svelte component
It adds a "three-dot" menu button with Popover, and delete confirmation Modal
-->
<script lang="ts">
  import { twMerge } from 'tailwind-merge';
  import { Button, Input, P, Popover } from 'flowbite-svelte';
  import { DotsVerticalOutline, ExclamationCircleOutline } from 'flowbite-svelte-icons';
  import { threadsStore } from '$stores';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { MAX_LABEL_SIZE } from '$constants';
  import { Modal } from 'flowbite-svelte';

  export let sClass: string =
    'flex items-center p-2 ps-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700';
  export let threadId: string;
  export let label: string = '';
  export let activeClass: string =
    'flex items-center p-2 ps-11 text-base font-normal text-gray-900 bg-gray-200 dark:bg-gray-700 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700';
  export let active: boolean = false;
  let deleteModalOpen = false;
  let editLabelText: string | undefined = label;
  let editLabelInputDisabled = false;

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

<li class="flex flex-grow justify-between">
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
      class={twMerge(
        active ? activeClass : sClass,
        'truncate',
        'flex-grow',
        'cursor-pointer',
        $$props.class
      )}
    >
      <P size="sm" class="truncate whitespace-nowrap">
        {label}
      </P>
    </button>
    <button
      data-testid={`thread-menu-btn-${label}`}
      id={`btn-${threadId}`}
      class={popperOpen && 'focus:rounded focus:bg-gray-400'}
    >
      <DotsVerticalOutline color="white" />
    </button>
    <Popover
      data-testid={'sidebar-popover'}
      class="w-32 border-none border-none text-sm font-light"
      defaultClass="p-0"
      placement="right"
      trigger="click"
      triggeredBy={`#btn-${threadId}`}
      arrow={false}
      on:show={() => {
        popperOpen = !popperOpen;
      }}
      ><div class="flex flex-col items-center gap-1">
        <Button size="xs" class="w-full" on:click={handleEditClick}>Edit</Button>
        <Button
          size="xs"
          class="w-full"
          on:click={(e) => {
            e.stopPropagation();
            deleteModalOpen = true;
          }}>Delete</Button
        >
      </div></Popover
    >
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
    <P size="xl" class="text-center dark:text-gray-400">
      Are you sure you want to delete your <strong>{label.substring(0, MAX_LABEL_SIZE)}</strong> chat?
    </P>
    <div class="flex justify-end gap-2">
      <Button color="alternative" size="sm">Cancel</Button>
      <Button color="red" on:click={handleDelete} size="sm">Delete</Button>
    </div>
  </div>
</Modal>
