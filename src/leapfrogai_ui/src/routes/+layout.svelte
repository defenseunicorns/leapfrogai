<script>
  import '../app.css';
  import { invalidate } from '$app/navigation';
  import { onMount } from 'svelte';
  import { Toasts } from '$components';
  import { page } from '$app/stores';
  import 'carbon-components-svelte/css/g90.css';
  import '../styles/main.scss';
  import '$webComponents/CodeBlock';
  export let data;

  let { supabase, session } = data;

  $: ({ supabase, session } = data);

  onMount(() => {
    const { data } = supabase.auth.onAuthStateChange((event, _session) => {
      if (_session?.expires_at !== session?.expires_at) {
        invalidate('supabase:auth');
      }
    });

    return () => data.subscription.unsubscribe();
  });
</script>

<svelte:head>
  <title>{$page.data.title || ''}</title>
</svelte:head>

<Toasts></Toasts>

<div class="content">
  <slot />
</div>

<style lang="scss">
  .content {
    height: calc(100vh - var(--header-height));
  }
</style>
