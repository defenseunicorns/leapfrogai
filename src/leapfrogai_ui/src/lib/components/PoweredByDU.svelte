<script>
  import doug from '$assets/Doug.png';
  import DefenseUnicorns from '$assets/DefenseUnicorns.png';
</script>

<div class="flex">
  <img alt="Doug" src={doug} class="icon" />
  <span class="legal">Powered By</span>
  <img alt="Defense Unicorns" src={DefenseUnicorns} class="wordmark" />
</div>

<style lang="scss">
  .flex {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.25rem;
    margin-top: 1rem;
  }
  .legal {
    font-size: 0.75rem;
    line-height: 1rem;
    font-weight: 400;
    letter-spacing: 0.32px;
  }
  .icon {
    height: var(--footer-height);
  }
  .wordmark {
    width: 6.75rem;
  }
</style>
