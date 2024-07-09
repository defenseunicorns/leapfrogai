<script lang="ts">
  import 'highlight.js/styles/atom-one-dark-reasonable.css';
  import DOMPurify from 'dompurify';
  export let code: string;
</script>

<!--eslint-disable-next-line svelte/no-at-html-tags -- We use DomPurity to sanitize the code snippet-->
{@html DOMPurify.sanitize(code)}
