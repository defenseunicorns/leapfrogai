<script lang="ts">
  import { LFHeader } from '$components';
  import type { LayoutData } from './$types';

  export let data: LayoutData;
</script>

<LFHeader isUsingOpenAI={data.isUsingOpenAI} />

<slot />
