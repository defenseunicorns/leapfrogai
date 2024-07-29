<script lang="ts">
  import { fade } from 'svelte/transition';
  import { goto, invalidate } from '$app/navigation';
  import { Avatar, Button, Card, Dropdown, DropdownItem, Modal } from 'flowbite-svelte';
  import { DotsHorizontalOutline, ExclamationCircleOutline } from 'flowbite-svelte-icons';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { threadsStore, toastStore } from '$stores';
  import { NO_SELECTED_ASSISTANT_ID } from '$constants';
  import type { LFAssistant } from '$lib/types/assistants';

  export let assistant: LFAssistant;

  let deleteModalOpen = false;

  const handleDelete = async () => {
    const res = await fetch('/api/assistants/delete', {
      method: 'DELETE',
      body: JSON.stringify({ id: assistant.id }),
      headers: {
        'Content-Type': 'application/json'
      }
    });
    if ($threadsStore.selectedAssistantId === assistant.id)
      threadsStore.setSelectedAssistantId(NO_SELECTED_ASSISTANT_ID);

    deleteModalOpen = false;

    if (res.ok) {
      await invalidate('lf:assistants');
      toastStore.addToast({
        kind: 'info',
        title: 'Assistant Deleted.',
        subtitle: `${assistant.name} Assistant deleted.`
      });
      return;
    }

    toastStore.addToast({
      kind: 'error',
      title: 'Error',
      subtitle: 'Error deleting Assistant.'
    });
  };
</script>

<div transition:fade={{ duration: 150 }}>
  <Card data-testid={`assistant-card-${assistant.name}`} padding="md" class="h-full">
    <div class="flex justify-end">
      <DotsHorizontalOutline data-testid="assistant-edit-icon" />
      <Dropdown class="w-36" data-testid="assistant-card-dropdown">
        <DropdownItem on:click={() => goto(`/chat/assistants-management/edit/${assistant.id}`)}
          >Edit</DropdownItem
        >
        <DropdownItem on:click={() => (deleteModalOpen = true)}>Delete</DropdownItem>
      </Dropdown>
    </div>

    <div class="flex flex-col items-center gap-2 pb-4">
      {#if assistant.metadata.avatar}
        <Avatar
          data-testid="assistant-card-avatar"
          size="md"
          src={`${assistant.metadata.avatar}?v=${new Date().getTime()}`}
        />
      {:else}
        <DynamicPictogram iconName={assistant.metadata.pictogram || 'default'} size="md" />
      {/if}
      <!--With fixed width and font sizes, there isn't a simple solution for multi line text ellipses, so doing it manually at specific character length instead-->
      <h5 class="mb-1 break-all text-xl font-medium text-gray-900 dark:text-white">
        {assistant.name && assistant.name.length > 20
          ? `${assistant.name.slice(0, 20)}...`
          : assistant.name}
      </h5>
      <span class="overflow-hidden break-all text-center text-sm text-gray-500 dark:text-gray-400">
        {assistant.description && assistant.description.length > 75
          ? `${assistant.description?.slice(0, 75)}...`
          : assistant.description}</span
      >
    </div>
  </Card>
</div>
<Modal
  bind:open={deleteModalOpen}
  autoclose
  title="Delete Assistant"
  data-testid="delete-assistant-modal"
>
  <div class="text-center">
    <ExclamationCircleOutline class="mx-auto mb-4 h-12 w-12 text-gray-400 dark:text-gray-200" />
    <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
      Are you sure you want to delete your
      <strong>{assistant.name}</strong>
      assistant?
    </h3>
    <Button color="red" class="me-2" on:click={handleDelete}>Delete</Button>
    <Button color="alternative">Cancel</Button>
  </div></Modal
>
