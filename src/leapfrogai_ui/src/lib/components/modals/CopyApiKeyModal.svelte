<script lang="ts">
  import { formatKeyLong } from '$helpers/apiKeyHelpers.js';
  import { calculateDays, formatDate } from '$helpers/dates.js';
  import { Button, Kbd, Label, Modal, P } from 'flowbite-svelte';
  import type { APIKeyRow } from '$lib/types/apiKeys';
  import CopyToClipboardBtn from '$components/CopyToClipboardBtn.svelte';

  export let copyKeyModalOpen: boolean;
  export let createdKey: APIKeyRow | null;

  let saveKeyModalRef: HTMLDivElement;

  const handleClose = () => {
    copyKeyModalOpen = false;
  };
</script>

<Modal
  bind:open={copyKeyModalOpen}
  autoclose
  title="Save secret key"
  on:close={handleClose}
  color="primary"
>
  {#if createdKey}
    <div class="flex flex-col gap-4">
      <P size="xl" class="text-center dark:text-gray-400">
        Please store this secret key in a safe and accessible place. For security purposes, it
        cannot be viewed again through your LeapfrogAI account. If you lose it, you'll need to
        create a new one.
      </P>
      <div class="flex w-full gap-2">
        <Kbd class="flex items-center px-2 py-1.5"
          >{formatKeyLong(createdKey.api_key, saveKeyModalRef?.offsetWidth || 200)}</Kbd
        >
        <CopyToClipboardBtn btnText="Copy" value={createdKey.api_key} toastTitle="API Key Copied" />
      </div>
      <div>
        <Label for="saved-expiration" class="mb-2 block">Expiration</Label>
        <P size="lg" class=" dark:text-gray-400">
          {`${calculateDays(createdKey.created_at, createdKey.expires_at)} days - ${formatDate(new Date(createdKey.expires_at * 1000))}`}
        </P>
      </div>
    </div>
  {/if}
  <div class="flex justify-end">
    <Button on:click={handleClose} size="sm">Close</Button>
  </div>
</Modal>
