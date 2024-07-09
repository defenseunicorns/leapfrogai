<script lang="ts">
  import DOMPurify from 'dompurify';
  export let code: string;
</script>

<!--eslint-disable-next-line svelte/no-at-html-tags -- We use DomPurity to sanitize the code snippet-->
{@html DOMPurify.sanitize(code)}
