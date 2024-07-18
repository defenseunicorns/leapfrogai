<script lang="ts">
  import { threadsStore, uiStore } from '$stores';
  import logo from '$assets/LeapfrogAI.png';
  import { Settings, UserAvatar } from 'carbon-icons-svelte';
  import { Button, Header, HeaderAction, HeaderUtilities } from 'carbon-components-svelte';
  import { Navbar, NavBrand, NavHamburger } from 'flowbite-svelte';
  import { CogOutline, UserCircleOutline } from 'flowbite-svelte-icons';

  export let isUsingOpenAI: boolean;

  let loading = false;
  let signOutForm: HTMLFormElement;

  let navClass = 'py-0';
  let navDivClass = 'flex flex-wrap justify-between items-center w-full';

  $: innerWidth = 0;

  const handleLogOut = () => {
    loading = true;
    signOutForm.submit();
    loading = false;
  };

  // We override the default behavior of the HeaderAction component to close other actions
  // when a new one is opened
  let activeHeaderAction: { [key: string]: boolean };
  $: activeHeaderAction = {
    user: false,
    settings: false
  };

  const setActiveHeaderAction = (headerActionName: keyof typeof activeHeaderAction) => {
    Object.keys(activeHeaderAction).forEach((key) => {
      activeHeaderAction[key] = key === headerActionName;
    });
  };
</script>

<svelte:window bind:innerWidth />

<header>
  <Navbar {navClass} {navDivClass} class="dark:bg-secondary-500">
    <NavBrand href="/chat">
      <img src={logo} class="w-[7.875rem]] h-[2.25rem]" alt="LeapfrogAI Logo" />
    </NavBrand>
    <div class="flex items-center lg:order-2">
      <Button>
        <CogOutline data-testid="header-settings-btn" />
      </Button>
      <Button>
        <UserCircleOutline data-testid="header-profile-btn" />
      </Button>

      <NavHamburger
        on:click={toggle}
        btnClass="inline-flex items-center p-2 ml-1 text-sm text-gray-500 rounded-lg lg:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
      />
    </div>
  </Navbar>
</header>
