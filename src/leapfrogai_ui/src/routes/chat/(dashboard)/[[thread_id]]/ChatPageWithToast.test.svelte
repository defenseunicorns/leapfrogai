<script lang="ts">
  import { Toasts } from '$components';
  import ChatPage from './+page.svelte';
  import type { PageData } from './$types';

  export let data: PageData;
</script>

<div>
  <Toasts />
  <ChatPage {data} />
</div>
