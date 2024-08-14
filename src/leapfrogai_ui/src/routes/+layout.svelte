<script>
  import '../app.css';
  import { invalidate } from '$app/navigation';
  import { onMount } from 'svelte';
  import { Toasts } from '$components';
  import { page } from '$app/stores';
  import '$webComponents/CodeBlock';
  import {browser} from "$app/environment";
  export let data;

  let { supabase, session } = data;

  $: ({ supabase, session } = data);

  let resetTimer = true;
  $: {
    if (resetTimer && browser) {
      console.log("setting refresh timeout")
      resetTimer = false;
      setTimeout(async () => {
        // const { data, error } = await supabase.auth.refreshSession();
        invalidate('supabase:auth');
        if (error) {
          console.error('Error refreshing session:', error);
        } else {
          console.log('Session refreshed:', data);
        }
        resetTimer = true
      }, 10 * 1000);
    }
  }


  onMount(() => {
    const { data } = supabase.auth.onAuthStateChange((event, newSession) => {
      // console.log('auth state change');
      // console.log('new session expires at', newSession?.expires_at);
      // console.log('session expires at', session?.expires_at);
      if(event === "TOKEN_REFRESHED"){
        return;
      }
      if (newSession?.expires_at !== session?.expires_at) {
        invalidate('supabase:auth');
      }
    });

    return () => data.subscription.unsubscribe();
  });
</script>

<svelte:head>
  <title>{$page.data.title || ''}</title>
</svelte:head>

<Toasts />
<div class="flex h-screen flex-col bg-gray-900">
  <slot />
</div>
