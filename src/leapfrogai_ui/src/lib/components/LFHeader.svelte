<script lang="ts">
  import logo from '$assets/LeapfrogAI.png';
  import { Drawer, Navbar, NavBrand } from 'flowbite-svelte';
  import { CogOutline, UserCircleOutline } from 'flowbite-svelte-icons';
  import IconButton from '$components/IconButton.svelte';
  import { sineIn } from 'svelte/easing';

  export let isUsingOpenAI: boolean;

  let loading = false;
  let signOutForm: HTMLFormElement;

  $: innerWidth = 0;

  const handleLogOut = () => {
    loading = true;
    signOutForm.submit();
    loading = false;
  };

  // We override the default behavior of the HeaderAction component to close other actions
  // when a new one is opened
  let headerActionHidden: { [key: string]: boolean };
  $: headerActionHidden = {
    user: true,
    settings: true
  };

  const openDrawer = (headerActionName: keyof typeof headerActionHidden) => {
    Object.keys(headerActionHidden).forEach((key) => {
      if (key === headerActionName) {
        headerActionHidden[key] = false;
      } else {
        headerActionHidden[key] = true;
      }
    });
  };

  let transitionParams = {
    x: 320,
    duration: 200,
    easing: sineIn
  };
</script>

<svelte:window bind:innerWidth />

<header>
  <Navbar fluid class="dark:bg-secondary-500 dark:border-primary-400 h-12 py-1 dark:border-b">
    <NavBrand href="/chat">
      <img src={logo} class="w-[7.875rem]] h-[2.25rem]" alt="LeapfrogAI Logo" />
    </NavBrand>
    <div class="flex items-center gap-x-2">
      <IconButton on:click={() => openDrawer('settings')}>
        <CogOutline data-testid="header-settings-btn" />
      </IconButton>

      <IconButton on:click={() => openDrawer('user')}>
        <UserCircleOutline data-testid="header-user-btn" />
      </IconButton>
    </div>
  </Navbar>

  <Drawer
    transitionType="fly"
    {transitionParams}
    bind:hidden={headerActionHidden.settings}
    placement="right"
    id="settings-drawer"
  >
    <div class="links-container">
      <a href="/chat/assistants-management" class="header-link" on:click={() => openDrawer('')}
        >Assistants Management</a
      >

      <a href="/chat/file-management" class="header-link" on:click={() => openDrawer('')}
        >File Management</a
      >
      {#if !isUsingOpenAI}
        <a href="/chat/api-keys" class="header-link" on:click={() => openDrawer('')}>API Keys</a>
      {/if}
    </div>
  </Drawer>
  <Drawer
    transitionType="fly"
    {transitionParams}
    bind:hidden={headerActionHidden.user}
    placement="right"
    id="user-drawer"
  >
    <div class="links-container">
      <form bind:this={signOutForm} method="post" action="/auth?/signout">
        <button class="header-link" aria-label="Log Out" disabled={loading} on:click={handleLogOut}
          >Log Out</button
        >
      </form>
    </div>
  </Drawer>
</header>

<style lang="scss">
  .links-container {
    display: flex;
    padding: 1rem;
    flex-direction: column;
    gap: 0.88rem;
  }

  .header-link {
    font-size: 0.875rem;
    line-height: 1.125rem;
    font-weight: 600;
    letter-spacing: 0.16px;
    cursor: pointer;
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    outline: inherit;
    text-decoration: none;
    &:hover {
      color: #ffffff;
    }
  }
</style>
