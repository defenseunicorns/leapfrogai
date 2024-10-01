<script lang="ts">
  import { goto } from '$app/navigation';
  import { assistantsStore } from '$stores';
  import { NO_SELECTED_ASSISTANT_ID } from '$constants';
  import { Button, Dropdown, DropdownItem } from 'flowbite-svelte';
  import { CheckOutline, ChevronDownOutline, UserAddSolid } from 'flowbite-svelte-icons';

  let assistantSelectDropdownOpen = false;

  $: selectedAssistantName =
    $assistantsStore.assistants.find(
      (assistant) => assistant.id === $assistantsStore.selectedAssistantId
    )?.name || 'No Assistant';

  const handleSelectAssistant = (e) => {
    e.preventDefault();
    const item = e.target.closest('button, [data-value]');
    if (item) {
      const selectedAssistantId = item.dataset.value;
      if ($assistantsStore.selectedAssistantId === selectedAssistantId) {
        assistantsStore.setSelectedAssistantId(NO_SELECTED_ASSISTANT_ID);
      } else {
        assistantsStore.setSelectedAssistantId(selectedAssistantId);
      }
    }
    assistantSelectDropdownOpen = false;
  };
</script>

<Button
  color="dark"
  class="max-h-[42px] w-48 flex-shrink-0 justify-between border border-gray-600 dark:bg-gray-700  dark:focus-within:ring-1 dark:focus-within:ring-blue-500"
  ><span class="truncate">{selectedAssistantName}</span><ChevronDownOutline
    class="ms-2 h-6 w-6 text-white dark:text-white"
    data-testid="assistants-select-btn"
  /></Button
>
<Dropdown
  bind:open={assistantSelectDropdownOpen}
  footerClass="overflow-hidden rounded-b-lg"
  class="h-[228px] w-56 overflow-y-auto text-sm"
>
  <div
    slot="header"
    class="flex items-center bg-gray-50 text-sm font-medium hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600"
  >
    <DropdownItem
      on:click={() => {
        assistantsStore.setSelectedAssistantId(NO_SELECTED_ASSISTANT_ID);
        assistantSelectDropdownOpen = false;
      }}
      class="flex justify-between"
      >No Assistant {#if $assistantsStore.selectedAssistantId === NO_SELECTED_ASSISTANT_ID}
        <CheckOutline data-testid="checked" />
      {/if}</DropdownItem
    >
  </div>
  {#each $assistantsStore.assistants as assistant (assistant.id)}
    <DropdownItem
      on:click={handleSelectAssistant}
      data-value={assistant.id}
      class="flex justify-between font-normal"
    >
      {assistant.name.length > 20 ? `${assistant.name.slice(0, 20)}...` : assistant.name}
      {#if $assistantsStore.selectedAssistantId === assistant.id}
        <CheckOutline data-testid="checked" />
      {/if}
    </DropdownItem>
  {/each}

  <div slot="footer" class="px-4 py-2.5">
    <button
      id="manage assistants"
      data-testid="assistants-management-btn"
      class="flex items-center gap-1 text-blue-500 dark:hover:text-blue-400"
      on:click={(e) => {
        e.preventDefault();
        goto('/chat/assistants-management');
      }}
    >
      <UserAddSolid />
      Manage Assistants
    </button>
  </div>
</Dropdown>
