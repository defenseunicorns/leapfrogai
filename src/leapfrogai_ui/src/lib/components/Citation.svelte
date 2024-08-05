<script lang="ts">
  import { browser } from '$app/environment';
  import { toastStore } from '$stores';
  import type { FileObject } from 'openai/resources/files';
  import { ArrowUpOutline } from 'flowbite-svelte-icons';
  export let file: FileObject;
  export let index: string;

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
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = file.filename;
      document.body.appendChild(a);
      a.click();

      if (res.headers.get('content-type') === 'application/pdf') {
        // Open in a new tab
        window.open(url, '_blank');
      }

      window.URL.revokeObjectURL(url); // avoid memory leaks
    }
  };
</script>

<button
  class="flex items-center justify-center gap-1"
  on:click={(e) => {
    e.preventDefault();
    handleClick();
  }}
>
  <span class="link">{`[${index}] ${file.filename}`}</span>
  <ArrowUpOutline class="link cursor-pointer" color="#78a9ff" />
</button>
