<script lang="ts">
  import { twMerge } from 'tailwind-merge';
  import { Button, Input, P, Popover } from 'flowbite-svelte';
  import { DotsVerticalOutline } from 'flowbite-svelte-icons';
  import { threadsStore } from '$stores';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { MAX_LABEL_SIZE } from '$constants';
  import { Modal } from 'carbon-components-svelte';

  export let sClass: string =
    'flex items-center p-2 ps-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700';
  export let threadId: string;
  export let label: string = '';
  export let activeClass: string =
    'flex items-center p-2 ps-11 text-base font-normal text-gray-900 bg-gray-200 dark:bg-gray-700 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700';
  export let active: boolean = false;
  let deleteModalOpen = false;
  let editLabelText: string | undefined;
  let editLabelInputDisabled = false;

  let lengthOverride = 'overflow-hidden text-ellipsis whitespace-nowrap';

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
    />
  {:else}
    <span
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
        lengthOverride,
        'flex-grow',
        'cursor-pointer',
        $$props.class
      )}
    >
      <P class="overflow-hidden text-ellipsis whitespace-nowrap">
        {label}
      </P>
    </span>
    <button id={`btn-${threadId}`} class={popperOpen && 'focus:rounded focus:bg-gray-400'}>
      <DotsVerticalOutline />
    </button>
    <Popover
      class="w-32 text-sm font-light"
      defaultClass="p-0"
      placement="right"
      trigger="click"
      triggeredBy={`#btn-${threadId}`}
      arrow={false}
      on:show={() => {
        console.log('on show');
        popperOpen = !popperOpen;
      }}
      ><div class="flex flex-col items-center gap-1">
        <Button color="alternative" size="xs" class="w-full" on:click={handleEditClick}>Edit</Button
        >
        <Button
          color="alternative"
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
  >Are you sure you want to delete your <strong>{label.substring(0, MAX_LABEL_SIZE)}</strong> chat?</Modal
>

<!--
@component
[Go to docs](https://flowbite-svelte.com/)
## Props
@prop export let sClass: string = 'flex items-center p-2 ps-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700';
@prop export let href: string = '';
@prop export let label: string = '';
@prop export let activeClass: string = 'flex items-center p-2 ps-11 text-base font-normal text-gray-900 bg-gray-200 dark:bg-gray-700 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700';
@prop export let active: boolean = false;
-->
