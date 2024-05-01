<script>
  import { goto } from '$app/navigation';
  import { Button, Search } from 'carbon-components-svelte';
  import { Add } from 'carbon-icons-svelte';
</script>

<div class="container">
  <div class="inner-container">
    <div class="title">Assistants Management</div>

    <div class="utils">
      <Search placeholder="Search" expanded size="sm" style="width: 20.5rem" />
      <Button
        kind="primary"
        size="small"
        icon={Add}
        on:click={() => goto('/chat/assistants-management/new')}>New assistant</Button
      >
    </div>
  </div>
</div>

<style lang="scss">
  .container {
    display: flex;
    justify-content: center;
  }
  .inner-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 80%;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }

  .utils {
    display: flex;
    justify-content: space-between;
  }

  .title {
    @include type.type-style('heading-05');
  }
</style>
