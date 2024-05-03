<script lang="ts">
  import { Content } from 'carbon-components-svelte';
  import { PoweredByDU } from '$components/index.js';
</script>

<Content>
  <div class="lf-content-container">
    <div class="slot-wrapper">
      <slot />
    </div>
    <div>
      <PoweredByDU />
    </div>
  </div>
</Content>

<style lang="scss">
  .slot-wrapper {
    height: 100%;
  }
  .lf-content-container {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
