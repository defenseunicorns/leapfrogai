<script lang="ts">
  import { threadsStore, uiStore } from '$stores';
  import logo from '$assets/LeapfrogAI.png';
  import { Button, Drawer, Navbar, NavBrand } from 'flowbite-svelte';
  import { BarsOutline, CloseOutline, CogOutline, UserCircleOutline } from 'flowbite-svelte-icons';
  import HeaderButton from '$components/HeaderButton.svelte';
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

  let drawerStyle = 'top-header text-white';
  let linkStyle = 'flex p-4 flex-col gap-3.5';
  let headerLinkStyle =
    'text-sm leading-5 font-semibold tracking-tight cursor-pointer bg-none text-inherit border-none p-0 outline-none hover:text-white';
  $: innerWidth = 0;
</script>

<svelte:window bind:innerWidth />

<header>
  <Navbar fluid class="h-header py-1 dark:bg-black">
    <NavBrand
      href={$threadsStore.lastVisitedThreadId
        ? `/chat/${$threadsStore.lastVisitedThreadId}`
        : '/chat'}
      data-testid="logo-link"
    >
      {#if innerWidth < 1056}
        <Button
          outline={true}
          class="mr-2 !p-2"
          on:click={(e) => {
            e.preventDefault();
            uiStore.setOpenSidebar(!$uiStore.openSidebar);
          }}
        >
          {#if $uiStore.openSidebar}
            <CloseOutline data-testid="close-sidebar-btn" />
          {:else}
            <BarsOutline data-testid="open-sidebar-btn" />
          {/if}
        </Button>
      {/if}
      <img src={logo} class="w-[7.875rem]] h-[2.25rem]" alt="LeapfrogAI Logo" />
    </NavBrand>
    <div class="flex items-center gap-x-2">
      <HeaderButton on:click={() => toggleDrawer('settings')}>
        <CogOutline data-testid="header-settings-btn" />
      </HeaderButton>

      <HeaderButton on:click={() => toggleDrawer('user')}>
        <UserCircleOutline data-testid="header-user-btn" />
      </HeaderButton>
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
    data-testid="settings-drawer"
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
    data-testid="user-drawer"
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
