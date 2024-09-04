<script lang="ts">
  import '../app.css';
  import { invalidate } from '$app/navigation';
  import { onMount } from 'svelte';
  import { Toasts } from '$components';
  import { page } from '$app/stores';
  import '$webComponents/CodeBlock';
  import { browser } from '$app/environment';
  import { filesStore, uiStore } from '$stores';
  import vectorStatusStore from '$stores/vectorStatusStore';

  export let data;

  let { supabase, session } = data;

  $: ({ supabase, session } = data);

  // Refresh token early so backend requests get token with enough time before expiration (for long processing ops)
  let startRefreshCountdown = true;
  $: {
    if (startRefreshCountdown && browser && session) {
      startRefreshCountdown = false;
      const expiresIn = session.expires_at - Math.floor(Date.now() / 1000); // seconds until expiration
      const refreshTime = expiresIn - 1200; // 20 minutes before expiration
      if (refreshTime > 0) {
        setTimeout(async () => {
          await supabase.auth.refreshSession();
          startRefreshCountdown = true;
        }, refreshTime * 1000);
      }
    }
  }

  const handleVectorStoreTableUpdate = (payload) => {
    const newFile = payload.new;
    if (payload.eventType === 'DELETE') {
      vectorStatusStore.removeVectorStoreStatusFromFile(
        payload.old.id,
        payload.old.vector_store_id
      );
    } else {
      vectorStatusStore.updateFileVectorStatus(newFile.id, newFile.vector_store_id, newFile.status);
    }
  };
  const handleFileTableUpdate = (payload) => {
    filesStore.updateWithUploadSuccess([payload.new]);
  };

  onMount(() => {
    let vectorStoreChannel;
    let fileChannel;
    const { data } = supabase.auth.onAuthStateChange((_, newSession) => {
      if (newSession?.expires_at !== session?.expires_at) {
        invalidate('supabase:auth');
      }
      if (!$uiStore.isUsingOpenAI) {
        //*** REALTIME LISTENERS ***//
        vectorStoreChannel = supabase
          .channel('vector_store_file')
          .on(
            'postgres_changes',
            { event: '*', schema: 'public', table: 'vector_store_file' },
            handleVectorStoreTableUpdate
          )
          .subscribe();
        fileChannel = supabase
          .channel('file_objects')
          .on(
            'postgres_changes',
            { event: 'INSERT', schema: 'public', table: 'file_objects' },
            handleFileTableUpdate
          )
          .subscribe();
        //*** END REALTIME LISTENERS ***//
      }
    });

    // Cleanup
    return () => {
      data.subscription.unsubscribe();
      if (!$uiStore.isUsingOpenAI) {
        supabase.removeChannel(vectorStoreChannel);
        supabase.removeChannel(fileChannel);
      }
    };
  });
</script>

<svelte:head>
  <title>{$page.data.title || ''}</title>
</svelte:head>

<Toasts />
<div class="flex h-screen flex-col bg-gray-900">
  <slot />
</div>
