<script lang="ts">
  import { Button, Spinner } from 'flowbite-svelte';
  import { FileExportOutline, FileImportOutline } from 'flowbite-svelte-icons';
  import { threadsStore, toastStore } from '$stores';
  import { threadsSchema } from '$schemas/threadSchema';
  import type { LFThread } from '$lib/types/threads';
  import LFFileUploadBtn from '$components/LFFileUploadBtn.svelte';

  let importing = false;

  const readFileAsJson = <T,>(file: File): Promise<T> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = (event: ProgressEvent<FileReader>) => {
        if (event.target && typeof event.target.result === 'string') {
          try {
            const jsonObject = JSON.parse(event.target.result);
            resolve(jsonObject);
          } catch (error) {
            reject(error);
          }
        }
      };
      reader.onerror = (error) => {
        reject(error);
      };
      reader.readAsText(file);
    });
  };

  const onUpload = async (files: FileList) => {
    importing = true;
    toastStore.addToast({
      kind: 'info',
      title: 'Info',
      subtitle: `Importing conversations. Conversations will populate shortly...`
    });
    let threads: LFThread[] = [];
    try {
      threads = await readFileAsJson(files[0]);
      await threadsSchema.validate(threads);
    } catch {
      toastStore.addToast({
        kind: 'error',
        title: 'Error',
        subtitle: `Threads are incorrectly formatted.`,
        timeout: 5000
      });
      importing = false;
      return;
    }
    await threadsStore.importThreads(threads);
    importing = false;
  };

  const onExport = () => {
    try {
      const dataStr =
        'data:text/json; charset=utf-8,' +
        encodeURIComponent(JSON.stringify($threadsStore.threads));
      const downloadAnchorNode = document.createElement('a');

      downloadAnchorNode.setAttribute('href', dataStr);
      downloadAnchorNode.setAttribute('download', 'conversations.json');
      document.body.appendChild(downloadAnchorNode);
      downloadAnchorNode.click();
      downloadAnchorNode.remove();
    } catch {
      toastStore.addToast({
        kind: 'error',
        title: 'Error',
        subtitle: `Error exporting threads.`
      });
    }
  };
</script>

<div class="flex flex-col gap-2">
  {#if importing}
    <Button outline disabled size="sm" class="flex w-full justify-between">
      Importing...<Spinner size="4" color="white" />
    </Button>
  {:else}
    <LFFileUploadBtn
      data-testid="import-chat-history-input"
      color="alternative"
      outline
      size="sm"
      on:change={(e) => onUpload(e.detail)}
      accept={['application/json']}
      disabled={importing}
      btnColor="alternative"
    >
      Import chat history <FileImportOutline /></LFFileUploadBtn
    >
  {/if}

  <Button id="export-btn" outline size="sm" color="alternative" on:click={onExport} class="w-full">
    <div class="flex w-full justify-between">
      Export chat history <FileExportOutline />
    </div>
  </Button>
</div>
