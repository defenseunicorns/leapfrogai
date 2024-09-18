<script lang="ts">
  import { Button, Dropdown, DropdownItem, Navbar, NavBrand } from 'flowbite-svelte';
  import { BarsOutline, CloseOutline, CogOutline, UserCircleOutline } from 'flowbite-svelte-icons';
  import { page } from '$app/stores';
  import { threadsStore, uiStore } from '$stores';
  import logo from '$assets/LeapfrogAI.png';

  let signOutForm: HTMLFormElement;

  let innerWidth: number;
  $: innerWidth;

  const threadId = $page.params.thread_id;

  const handleLogOut = (e) => {
    e.preventDefault();

    signOutForm.submit();
  };
</script>

<svelte:window bind:innerWidth />

<header>
  <Navbar fluid class="h-header border-b border-gray-700 py-1 dark:bg-gray-800">
    <NavBrand
      href={$threadsStore.lastVisitedThreadId
        ? `/chat/${$threadsStore.lastVisitedThreadId}`
        : '/chat'}
      data-testid="logo-link"
    >
      {#if innerWidth !== undefined && innerWidth < 1024 && ($page.url.pathname === '/chat' || $page.url.pathname === `/chat/${threadId}`)}
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
    <div id="header-btns-container" class="flex gap-4">
      <CogOutline
        data-testid="header-settings-btn"
        class="settings-menu cursor-pointer dark:text-white"
      />
      <Dropdown triggeredBy=".settings-menu" data-testid="settings-dropdown" classContainer="z-max">
        <DropdownItem href="/chat/assistants-management">Assistants Management</DropdownItem>
        <DropdownItem href="/chat/file-management">File Management</DropdownItem>
        {#if !$uiStore.isUsingOpenAI}
          <DropdownItem href="/chat/api-keys">API Keys</DropdownItem>
        {/if}
      </Dropdown>

      <UserCircleOutline
        data-testid="header-profile-btn"
        class="profile-menu cursor-pointer dark:text-white"
      />
      <Dropdown triggeredBy=".profile-menu" data-testid="profile-dropdown" classContainer="z-max">
        <DropdownItem on:click={handleLogOut}
          >Log Out <form bind:this={signOutForm} method="post" action="/auth?/signout" />
        </DropdownItem>
      </Dropdown>
    </div>
  </Navbar>
</header>
