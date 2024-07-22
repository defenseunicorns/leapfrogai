<script lang="ts">
  import { goto } from '$app/navigation';
  import { threadsStore } from '$stores';
  import { NO_SELECTED_ASSISTANT_ID } from '$constants';
  import { Button, Dropdown, DropdownItem } from 'flowbite-svelte';
  import { CheckOutline, ChevronDownOutline, UserSettingsOutline } from 'flowbite-svelte-icons';
  import type { Assistant } from 'openai/resources/beta/assistants';

  export let assistants: Assistant[] = [];

  let assistantSelectDropdownOpen = false;

  $: selectedAssistantName =
    assistants.find((assistant) => assistant.id === $threadsStore.selectedAssistantId)?.name ||
    'Select assistant...';

  const handleSelectAssistant = (e) => {
    e.preventDefault();
    const item = e.target.closest('button, [data-value]');
    if (item) {
      const selectedAssistantId = item.dataset.value;
      threadsStore.setSelectedAssistantId(selectedAssistantId);
    }
    assistantSelectDropdownOpen = false;
  };
</script>

<Button class="w-48 justify-between"
  >{selectedAssistantName}<ChevronDownOutline
    class="ms-2 h-6 w-6 text-white dark:text-white"
    data-testid="assistants-select-btn"
  /></Button
>
<Dropdown bind:open={assistantSelectDropdownOpen} class="h-44 overflow-y-auto px-3 pb-3 text-sm">
  <div slot="header" class="p-3">
    <Button
      id="manage assistants"
      data-testid="assistants-management-btn"
      on:click={(e) => {
        e.preventDefault();
        goto('/chat/assistants-management');
      }}
    >
      <UserSettingsOutline />
      Manage Assistants
    </Button>
  </div>
  {#each assistants as assistant (assistant.id)}
    <DropdownItem
      on:click={handleSelectAssistant}
      data-value={assistant.id}
      class="flex justify-between"
    >
      {assistant.name}
      {#if $threadsStore.selectedAssistantId === assistant.id}
        <CheckOutline />
      {/if}
    </DropdownItem>
  {/each}
  <div
    slot="footer"
    class="-mb-1 flex items-center bg-gray-50 p-3 text-sm font-medium hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600"
  >
    <DropdownItem
      on:click={() => {
        threadsStore.setSelectedAssistantId(NO_SELECTED_ASSISTANT_ID);
        assistantSelectDropdownOpen = false;
      }}
      class="flex justify-between"
      >None {#if $threadsStore.selectedAssistantId === NO_SELECTED_ASSISTANT_ID}
        <CheckOutline />
      {/if}</DropdownItem
    >
  </div>
</Dropdown>
