<script lang="ts">
  import { env } from '$env/dynamic/public';
  import { fade } from 'svelte/transition';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { User } from 'carbon-icons-svelte';
  import { ClickableTile } from 'carbon-components-svelte';

  export let assistant: Assistant;
</script>

<div class="assistant-tile" transition:fade={{ duration: 70 }}>
  <ClickableTile>
    {#if assistant.metadata.avatar}
      <img
        src={`${env.PUBLIC_SUPABASE_URL}/storage/v1/object/public/assistant_avatars/${assistant.metadata.avatar}`}
        alt="avatar"
        width="40px"
        height="40px"
        style="border-radius: 50%;"
      />
    {:else if assistant.metadata.pictogram}
      <DynamicPictogram iconName={assistant.metadata.pictogram} />
    {:else}
      <User width="40px" height="40px" />
    {/if}
    <div class="name">{assistant.name}</div>
    <!--There isn't a simple solution for multi line text ellipses, so doing it manually at specific character length instead-->
    <div class="description">
      {assistant.description && assistant.description.length > 73
        ? `${assistant.description?.slice(0, 73)}...`
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
</style>
