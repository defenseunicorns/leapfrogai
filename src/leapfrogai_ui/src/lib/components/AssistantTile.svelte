<script lang="ts">
  import { goto, invalidateAll } from '$app/navigation';
  import { env } from '$env/dynamic/public';
  import { fade } from 'svelte/transition';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { Modal, OverflowMenu, OverflowMenuItem, Tile } from 'carbon-components-svelte';
  import { toastStore } from '$stores';
  import { Edit, TrashCan } from 'carbon-icons-svelte';

  export let assistant: Assistant;

  let deleteModalOpen = false;

  const handleDelete = async () => {
    const res = await fetch('/api/assistants/delete', {
      method: 'DELETE',
      body: JSON.stringify({ id: assistant.id }),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    deleteModalOpen = false;

    if (res.ok) {
      await invalidateAll();
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

<div
  class="assistant-tile"
  transition:fade={{ duration: 70 }}
  data-testid={`assistant-tile-${assistant.name}`}
>
  <Tile>
    <div class="overflow-menu-container">
      <OverflowMenu flipped size="sm" data-testid="overflow-menu">
        <OverflowMenuItem on:click={() => goto(`/chat/assistants-management/edit/${assistant.id}`)}>
          <div class="overflow-menu-item">
            Edit <Edit />
          </div>
        </OverflowMenuItem>
        <OverflowMenuItem on:click={() => (deleteModalOpen = true)}>
          <div class="overflow-menu-item">
            Delete <TrashCan />
          </div></OverflowMenuItem
        >
      </OverflowMenu>
    </div>
    {#if assistant.metadata.avatar}
      <div class="mini-avatar-container" data-testid="mini-avatar-container">
        <div
          class="mini-avatar-image"
          style={`background-image: url(${env.PUBLIC_SUPABASE_URL}/storage/v1/object/public/assistant_avatars/${assistant.metadata.avatar}?v=${new Date().getTime()}`}
        />
      </div>
    {:else}
      <DynamicPictogram iconName={assistant.metadata.pictogram || 'default'} />
    {/if}
    <div class="name">{assistant.name}</div>
    <!--There isn't a simple solution for multi line text ellipses, so doing it manually at specific character length instead-->
    <div class="description">
      {assistant.description && assistant.description.length > 62
        ? `${assistant.description?.slice(0, 62)}...`
        : assistant.description}
    </div>
  </Tile>
  <Modal
    danger
    bind:open={deleteModalOpen}
    modalHeading="Delete Assistant"
    primaryButtonText="Delete"
    secondaryButtonText="Cancel"
    on:click:button--secondary={() => (deleteModalOpen = false)}
    on:submit={() => handleDelete()}
  >
    <p>
      Are you sure you want to delete your
      <span style="font-weight: bold">{assistant.name}</span>
      assistant?
    </p>
  </Modal>
</div>

<style lang="scss">
  .name {
    @include type.type-style('heading-03');
  }
  .description {
    @include type.type-style('body-01');
    overflow: hidden;
  }

  .assistant-tile {
    position: relative;
    width: 288px;
    height: 172px;
    :global(.bx--tile) {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-around;
      text-align: center;
      gap: layout.$spacing-05;
      padding: 1rem;
      overflow: hidden;
      width: 100%;
      height: 100%;
    }

    .overflow-menu-container {
      position: absolute;
      top: 0.5rem;
      right: 0.5rem;

      .overflow-menu-item {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
    }
  }

  .mini-avatar-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;

    .mini-avatar-image {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
    }
  }
</style>
