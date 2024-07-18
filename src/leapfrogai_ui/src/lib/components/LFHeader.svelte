<script lang="ts">
  import logo from '$assets/LeapfrogAI.png';
  import { Drawer, Navbar, NavBrand } from 'flowbite-svelte';
  import { CogOutline, UserCircleOutline } from 'flowbite-svelte-icons';
  import IconButton from '$components/IconButton.svelte';
  import { sineIn } from 'svelte/easing';

  export let isUsingOpenAI: boolean;

  let loading = false;
  let signOutForm: HTMLFormElement;
  let transitionParams = {
    x: 320,
    duration: 200,
    easing: sineIn
  };

  $: activeDrawer = '';

  const handleLogOut = () => {
    loading = true;
    signOutForm.submit();
    loading = false;
  };

  const toggleDrawer = (name: string) => {
    if (activeDrawer === name) activeDrawer = '';
    else activeDrawer = name;
  };

  let drawerStyle = 'top-header dark:bg-primary-500';
  let linkStyle = 'flex p-4 flex-col gap-3.5';
  let headerLinkStyle =
    'text-sm leading-5 font-semibold tracking-tight cursor-pointer bg-none text-inherit border-none p-0 outline-none hover:text-white';
</script>

<!-- TODO - border-bottom is not showing for the nav-->
<header>
  <Navbar
    fluid
    class="fixed start-0 top-0 z-20 h-header py-1 dark:border-b dark:border-primary-400 dark:bg-secondary-500"
  >
    <NavBrand href="/chat">
      <img src={logo} class="w-[7.875rem]] h-[2.25rem]" alt="LeapfrogAI Logo" />
    </NavBrand>
    <div class="flex items-center gap-x-2">
      <IconButton on:click={() => toggleDrawer('settings')}>
        <CogOutline data-testid="header-settings-btn" />
      </IconButton>

      <IconButton on:click={() => toggleDrawer('user')}>
        <UserCircleOutline data-testid="header-user-btn" />
      </IconButton>
    </div>
  </Navbar>

  <Drawer
    transitionType="fly"
    {transitionParams}
    hidden={activeDrawer !== 'settings'}
    placement="right"
    backdrop={false}
    class={drawerStyle}
    id="settings-drawer"
  >
    <div class={linkStyle}>
      <a
        href="/chat/assistants-management"
        class={headerLinkStyle}
        on:click={() => toggleDrawer('')}>Assistants Management</a
      >

      <a href="/chat/file-management" class={headerLinkStyle} on:click={() => toggleDrawer('')}
        >File Management</a
      >
      {#if !isUsingOpenAI}
        <a href="/chat/api-keys" class={headerLinkStyle} on:click={() => toggleDrawer('')}
          >API Keys</a
        >
      {/if}
    </div>
  </Drawer>
  <Drawer
    transitionType="fly"
    {transitionParams}
    hidden={activeDrawer !== 'user'}
    placement="right"
    backdrop={false}
    class={drawerStyle}
    id="user-drawer"
  >
    <div class={linkStyle}>
      <form bind:this={signOutForm} method="post" action="/auth?/signout">
        <button
          class={headerLinkStyle}
          aria-label="Log Out"
          disabled={loading}
          on:click={handleLogOut}>Log Out</button
        >
      </form>
    </div>
  </Drawer>
</header>
