<script lang="ts">
  import { browser } from '$app/environment';
  import { toastStore } from '$stores';
  import type { FileObject } from 'openai/resources/files';
  import { ArrowUpOutline } from 'flowbite-svelte-icons';
  import { onDestroy } from 'svelte';
  export let file: FileObject;
  export let index: string;

  let expanded = false;
  let url: string;

  const handleClick = async () => {
    if (browser) {
      const res = await fetch(`/api/files/${file.id}`);
      if (!res.ok) {
        toastStore.addToast({
          kind: 'error',
          title: 'Error Downloading File',
          subtitle: `Please try again or contact support.`
        });
        return;
      }

      const blob = await res.blob();
      url = window.URL.createObjectURL(blob);
      // const a = document.createElement('a');
      // a.style.display = 'none';
      // a.href = url;
      // a.download = file.filename;
      // document.body.appendChild(a);
      // a.click();
      //
      // if (res.headers.get('content-type') === 'application/pdf') {
      //   // Open in a new tab
      //   window.open(url, '_blank');
      // }

      // window.URL.revokeObjectURL(url); // avoid memory leaks
    }
  };

  onDestroy(() => {
    if (url) window.URL.revokeObjectURL(url); // avoid memory leaks
  });
</script>

<button
  class="flex items-center justify-center gap-1"
  on:click={(e) => {
    e.preventDefault();
    expanded = !expanded;
    handleClick();
  }}
>
  <span class="link">{`[${index}] ${file.filename}`}</span>
  <ArrowUpOutline class="link cursor-pointer" color="#78a9ff" />
</button>
{#if expanded && url}
  <div class="relative h-0 w-full pb-[33%]">
    <iframe src={url} class="absolute left-0 top-0 h-full w-full border-0" />
  </div>
{/if}
