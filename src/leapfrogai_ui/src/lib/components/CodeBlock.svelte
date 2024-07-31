<svelte:options customElement="code-block-2" />

<script lang="ts">
  import { toastStore } from '$stores';
  import { Button } from 'flowbite-svelte';
  import { FileCopyOutline } from 'flowbite-svelte-icons';
  import { unsafeHTML } from 'lit/directives/unsafe-html.js';

  export let code: string;
  export let language: string;

  const removeHtml = () => {
    const tmp = document.createElement('DIV');
    tmp.innerHTML = this.code;
    return tmp.textContent || tmp.innerText || '';
  };

  const handleClick = async () => {
    await navigator.clipboard.writeText(removeHtml());
    toastStore.addToast({
      kind: 'info',
      title: 'Code Copied'
    });
  };
</script>

<div class="flex w-full flex-col overflow-hidden rounded-md border bg-gray-200">
  <div class="flex items-center justify-between rounded-t-md bg-gray-800 px-1 py-2">
    <span>${language}</span>
    <div class="centered-flexbox">
      <Button data-testid="copy-code-btn" color="alternative" on:click={handleClick}>
        <span>Copy</span>
        <FileCopyOutline />
      </Button>
    </div>
  </div>
  <div class="code-block-inner">${unsafeHTML(DOMPurify.sanitize(code))}</div>
</div>
