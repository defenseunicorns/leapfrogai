<script>
  import '../app.css';
  import { invalidate } from '$app/navigation';
  import { onMount } from 'svelte';
  import { Toasts } from '$components';
  import { page } from '$app/stores';
  import '$webComponents/CodeBlock';
  import { browser } from '$app/environment';
  export let data;

  let { supabase, session } = data;

  $: ({ supabase, session } = data);

  // let resetTimer = true;
  // $: {
  //   if (resetTimer && browser) {
  //     const expiresIn = session.expires_at - Math.floor(Date.now() / 1000); // seconds until expiration
  //     const refreshTime = expiresIn - 180; // 3 minutes before expiration
  //     console.log('expires in', expiresIn);
  //     console.log('refreshTime', refreshTime);
  //     console.log('setting refresh timeout');
  //     resetTimer = false;
  //     if (refreshTime > 0) {
  //       setTimeout(async () => {
  //         const { data, error } = await supabase.auth.refreshSession();
  //         // invalidate('supabase:auth');
  //         if (error) {
  //           console.error('Error refreshing session:', error);
  //         } else {
  //           console.log('Session refreshed:', data);
  //         }
  //         resetTimer = true;
  //       }, refreshTime * 1000);
  //     }
  //   }
  // }

  onMount(() => {
    const { data } = supabase.auth.onAuthStateChange((event, newSession) => {
      console.log('new session expires at', new Date(newSession?.expires_at * 1000));
      console.log('session expires at', new Date(session?.expires_at * 1000));
      if (event === 'TOKEN_REFRESHED') {
        console.log('token refreshed', new Date());
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
