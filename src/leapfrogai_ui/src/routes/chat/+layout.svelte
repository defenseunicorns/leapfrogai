<script lang="ts">
  import { LFHeader } from '$components';
</script>

<LFHeader />

<slot />

<style lang="scss">
  :global(.bx--content) {
    padding: 1rem !important;
  }
</style>
