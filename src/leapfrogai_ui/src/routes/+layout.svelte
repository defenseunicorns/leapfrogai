<script>
  import '../app.css';
  import { invalidate } from '$app/navigation';
  import { onMount } from 'svelte';
  import { Toasts } from '$components';
  import { page } from '$app/stores';
  import '$webComponents/CodeBlock';
  export let data;

  let { supabase, session } = data;

  $: ({ supabase, session } = data);

  onMount(() => {
    const { data } = supabase.auth.onAuthStateChange((_, newSession) => {
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

<div class="flex flex-col h-screen max-h-screen">
  <slot />
</div>
