<script lang="ts">
  import { env } from '$env/dynamic/public';
  import { fade } from 'svelte/transition';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { ClickableTile } from 'carbon-components-svelte';

  export let assistant: Assistant;
</script>

<div class="assistant-tile" transition:fade={{ duration: 70 }}>
  <ClickableTile>
    {#if assistant.metadata.avatar}
      <div class="mini-avatar-container" data-testid="mini-avatar-container">
        <div
          class="mini-avatar-image"
          style={`background-image: url(${env.PUBLIC_SUPABASE_URL}/storage/v1/object/public/assistant_avatars/${assistant.metadata.avatar}`}
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
  </ClickableTile>
</div>

<style lang="scss">
  .name {
    @include type.type-style('heading-03');
  }
  .description {
    @include type.type-style('body-01');
    line-height: 1em;
    height: 2em;
    overflow: hidden;
  }

  .assistant-tile {
    :global(.bx--tile) {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-around;
      text-align: center;
      gap: layout.$spacing-05;
      padding: 1rem;
      width: 288px;
      height: 172px;
      overflow: hidden;
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
