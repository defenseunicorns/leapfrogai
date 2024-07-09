<svelte:options customElement={{ tag: 'code-block', shadow: 'none' }} />

<!--
The markdown-it highlight option used in Message.svelte does not allow us to insert normal Svelte components in the
<pre><code>... block that it returns. This CodeBlock.svelte component is instead used as a web component within that
function to properly render the code blocks with highlighting and a copy button.
We have to forgo shadow root creation so that styles are no longer encapsulated (e.g. shadow: 'none') in the
customElement definition above.
In order to access styles from highlight.js and carbon, we import those sub-components into this one.
Trying to use the styles from within this component will not work.
-->
<script lang="ts">
  import CopyToClipboardBtn from '$components/CopyToClipboardBtn.svelte';
  import HighlightedCode from '$components/HighlightedCode.svelte';

  export let code: string;
  export let lang: string;

  const removeHtml = () => {
    let tmp = document.createElement('DIV');
    tmp.innerHTML = code;
    return tmp.textContent || tmp.innerText || '';
  };

  $: copyCode = removeHtml();
</script>

<div class="code-block">
  <div class="code-block-header">
    <span>{lang}</span>
    <div class="centered-flexbox">
      <CopyToClipboardBtn value={copyCode} toastTitle="Code Copied" />
    </div>
  </div>
  <div class="code-block-inner">
    <HighlightedCode {code} />
  </div>
</div>

<slot />

<style lang="scss">
  .centered-flexbox {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .code-block {
    background-color: themes.$background;
    border: 0.5px solid themes.$border-subtle-00;
    border-radius: 0.375rem;
  }
  .code-block-inner {
    overflow-y: auto;
    padding: 1rem;
  }
  .code-block-header {
    display: flex;
    align-items: center;
    position: relative;
    background-color: themes.$background-hover;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    font-size: 0.75rem;
    justify-content: space-between;
    border-top-left-radius: 0.375rem;
    border-top-right-radius: 0.375rem;
  }
</style>
