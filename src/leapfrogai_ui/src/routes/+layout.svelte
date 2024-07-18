<script>
  import '../app.css';
  import { invalidate } from '$app/navigation';
  import { onMount } from 'svelte';
  import { Toasts } from '$components';
  import { page } from '$app/stores';
  import 'carbon-components-svelte/css/g90.css';
  import '../styles/main.scss';
  import { Theme } from 'carbon-components-svelte';
  import '$webComponents/CodeBlock';
  export let data;
  let theme = 'g90';

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

<Theme bind:theme></Theme>

<Toasts></Toasts>

<slot></slot>

<style>
  :global(.bx--content) {
    height: calc(100vh - var(--header-height));
    padding-bottom: 1rem;
  }
</style>
