<script lang="ts">
  export let tinted: boolean = false;
</script>

<section class={tinted ? 'bg-gray-50 dark:bg-gray-800' : ''}>
  <div class="max-w-8xl mx-auto px-4 py-8 lg:px-20 {$$props.class ?? ''}">
    <slot />
  </div>
</section>
