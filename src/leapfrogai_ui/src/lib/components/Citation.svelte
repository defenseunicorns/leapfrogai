<script lang="ts">
  import { onDestroy } from 'svelte';
  import {
    ArrowDownOutline,
    ArrowUpOutline,
    ArrowUpRightFromSquareOutline,
    DownloadOutline
  } from 'flowbite-svelte-icons';
  import { Button } from 'flowbite-svelte';
  import { twMerge } from 'tailwind-merge';
  import { browser } from '$app/environment';
  import { toastStore, uiStore } from '$stores';
  import type { FileObject } from 'openai/resources/files';
  import FileProcessingPlaceholder from '$components/FileProcessingPlaceholder.svelte';
  import { FILE_MIME_TYPES_FOR_CONVERSION } from '$constants';
  import {
    CONVERT_FILE_ERROR_MSG_TOAST,
    FILE_DOWNLOAD_ERROR_MSG_TOAST,
    OPENAI_DOWNLOAD_DISABLED_MSG_TOAST
  } from '$constants/toastMessages';

  export let file: FileObject;
  export let index: string;

  // TODO - debug blog on deployed app vs local (different encoding or font family?)

  let expanded = false;
  let url: string;
  let processing = false;

  const handleFileError = () => {
    processing = false;
    toastStore.addToast({
      ...FILE_DOWNLOAD_ERROR_MSG_TOAST
    });
  };

  const handleClick = async () => {
    if (browser) {
      if ($uiStore.isUsingOpenAI) {
        toastStore.addToast({
          ...OPENAI_DOWNLOAD_DISABLED_MSG_TOAST
        });
        return;
      }

      processing = true;
      expanded = !expanded;
      if (url) {
        window.URL.revokeObjectURL(url);
        url = '';
      } // remove old url, prevent memory leaks

      try {
        const res = await fetch(`/api/files/${file.id}`);
        if (!res.ok) {
          handleFileError();
          return;
        }

        let contentType = res.headers.get('content-type');

        // content type can include charset, removing that here (ex. text.plain; charset=UTF-8)
        if (contentType?.includes('text/plain')) contentType = 'text/plain';

        if (!contentType) {
          handleFileError();
          return;
        }

        // pdf
        if (contentType === 'application/pdf') {
          const blob = await res.blob();
          url = window.URL.createObjectURL(blob);
          processing = false;
          return;
        }

        // non-pdf
        if (FILE_MIME_TYPES_FOR_CONVERSION.includes(contentType)) {
          const convertRes = await fetch('/api/files/convert', {
            method: 'POST',
            body: JSON.stringify({ id: file.id })
          });
          if (!convertRes.ok) {
            handleFileError();
            return;
          }
          const convertedFileBlob = await convertRes.blob();
          url = window.URL.createObjectURL(convertedFileBlob);
          processing = false;
          return;
        } else {
          toastStore.addToast({
            ...CONVERT_FILE_ERROR_MSG_TOAST
          });
          processing = false;
          return;
        }
      } catch {
        handleFileError();
      }
    }
  };

  const handleDownload = (e) => {
    e.preventDefault();

    if ($uiStore.isUsingOpenAI) {
      toastStore.addToast({
        kind: 'warning',
        title: 'File download disabled when using OpenAI',
        subtitle: `OpenAI does not allow download of files with purpose 'assistants'`
      });
      return;
    }
    if (url) {
      // download only
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = file.filename;
      document.body.appendChild(a);
      a.click();

      toastStore.addToast({
        kind: 'success',
        title: 'Downloaded Successfully',
        subtitle: `${file.filename} downloaded successfully.`
      });
    }
  };

  const handleOpenInNewTab = (e) => {
    e.preventDefault();
    if (url) window.open(url, '_blank');
    else {
      toastStore.addToast({
        kind: 'error',
        title: 'Error Opening File'
      });
    }
  };

  onDestroy(() => {
    if (url) window.URL.revokeObjectURL(url); // avoid memory leaks
  });
</script>

<button
  data-testid={`${file.id}-citation-btn`}
  on:click={(e) => {
    e.preventDefault();
    handleClick();
  }}
  class={twMerge(
    'link flex items-center justify-center gap-1',
    expanded && 'mb-1 !text-white underline'
  )}
>
  <span class={expanded && 'border-b-2'}>{`[${index}] ${file.filename}`}</span>
  {#if expanded}
    <ArrowDownOutline class="link cursor-pointer !text-white" />
  {:else}
    <ArrowUpOutline class="link cursor-pointer" />
  {/if}
</button>
{#if expanded && processing}
  <FileProcessingPlaceholder imgOnly class="mb-2 mt-2 h-12" data-testid="file-processing-spinner" />
{/if}
{#if expanded && url}
  <div class="relative mb-4 h-0 w-full pb-[33%]">
    <iframe
      src={`${url}#toolbar=0`}
      title={`${file.id}-iframe`}
      class="absolute left-0 top-0 h-full w-full border-2 border-gray-200"
    />
    <div class="absolute bottom-2 right-8 flex gap-2">
      <Button
        data-testid="file-download-btn"
        outline
        size="large"
        class="!p-2"
        on:click={handleDownload}><DownloadOutline /></Button
      >
      {#if file.filename.endsWith('.pdf')}
        <Button
          data-testid="file-open-new-tab-btn"
          outline
          size="large"
          class="!p-2"
          on:click={handleOpenInNewTab}><ArrowUpRightFromSquareOutline /></Button
        >
      {/if}
    </div>
  </div>
{/if}
