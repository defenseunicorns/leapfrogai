<script lang="ts">
  import { FileUploaderButton } from 'carbon-components-svelte';
  import Pictograms from '$components/Pictograms.svelte';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { AVATAR_FILE_SIZE_ERROR_TEXT, MAX_AVATAR_SIZE, NO_FILE_ERROR_TEXT } from '$lib/constants';
  import { Avatar, Button, Modal, P, Radio } from 'flowbite-svelte';
  import { twMerge } from 'tailwind-merge';
  import { EditOutline, TrashBinOutline } from 'flowbite-svelte-icons';

  export let form;
  export let files: File[];
  export let selectedPictogramName: string;

  let originalAvatar = $form.avatar;
  let tempFiles: File[] = [];
  let tempPictogram = selectedPictogramName || 'default';
  let modalOpen = false;
  let selectedRadioButton: 'upload' | 'pictogram' = originalAvatar ? 'upload' : 'pictogram';
  let shouldValidate = false;
  let fileUploaderRef: HTMLInputElement;
  let errorMsg = '';
  let skipCloseActions = false;

  $: avatarToShow = tempFiles?.length > 0 ? URL.createObjectURL(tempFiles[0]) : $form.avatar;
  $: fileNotUploaded = !tempFiles[0]; // if on upload tab, you must upload a file to enable save
  $: fileTooBig = tempFiles[0]?.size > MAX_AVATAR_SIZE;
  $: hideUploader = avatarToShow ? true : tempFiles.length > 0;

  const handleRemove = () => {
    tempFiles = [];
    $form.avatar = '';
    tempPictogram = selectedPictogramName || 'default';
    shouldValidate = false;
  };

  const handleClose = () => {
    if (!skipCloseActions) {
      shouldValidate = false;
      modalOpen = false;
      $form.avatar = originalAvatar;
      tempPictogram = selectedPictogramName; // reset to original pictogram
      if (files?.length > 0) {
        tempFiles = [...files]; // reset to original file
      } else {
        tempFiles = [];
      }
    }
    skipCloseActions = false;
  };

  const handleChangeAvatar = () => {
    fileUploaderRef.click(); // re-open upload dialog
  };

  const handleSubmit = () => {
    skipCloseActions = true;
    shouldValidate = true;

    if (selectedRadioButton === 'upload') {
      if (fileNotUploaded) {
        errorMsg = NO_FILE_ERROR_TEXT;
        return;
      }
      if (fileTooBig) {
        errorMsg = AVATAR_FILE_SIZE_ERROR_TEXT;
        return;
      }
      files = [...tempFiles];
      modalOpen = false;
      shouldValidate = false;
    } else {
      // pictogram tab
      selectedPictogramName = tempPictogram;
      files = []; // remove saved avatar
      tempFiles = [];
      $form.avatar = '';

      modalOpen = false;
      shouldValidate = false;
    }
  };
</script>

<div>
  <button
    tabindex="0"
    on:click|preventDefault={() => (modalOpen = true)}
    data-testid="mini-avatar-container"
  >
    {#if avatarToShow}
      <Avatar src={avatarToShow} />
    {:else}
      <DynamicPictogram iconName={tempPictogram} size="md" />
    {/if}
  </button>
  <Modal
    bind:open={modalOpen}
    autoclose
    on:close={handleClose}
    on:submit={handleSubmit}
    title="Avatar Image"
    class="overflow-hidden"
  >
    <div class="flex flex-col gap-2">
      <div class="flex gap-4">
        <Radio
          name="Pictogram"
          checked={selectedRadioButton === 'pictogram'}
          on:click={() => (selectedRadioButton = 'pictogram')}>Pictogram</Radio
        >
        <Radio
          name="Upload"
          checked={selectedRadioButton === 'upload'}
          on:click={() => (selectedRadioButton = 'upload')}>Upload</Radio
        >
      </div>
      <span class={twMerge(selectedRadioButton === 'upload' && 'hidden')}>
        <Pictograms bind:selectedPictogramName={tempPictogram} />
      </span>

      <div class={twMerge('flex flex-col gap-2', selectedRadioButton === 'pictogram' && 'hidden')}>
        {#if avatarToShow}
          <Avatar src={avatarToShow} />
        {/if}

        <div class={twMerge('flex flex-col gap-2', hideUploader ? 'hidden' : 'block')}>
          <P>Upload image</P>
          <P size="sm">Supported file types are .jpg and .png.</P>
          <FileUploaderButton
            bind:ref={fileUploaderRef}
            bind:files={tempFiles}
            name="avatarFile"
            kind="tertiary"
            labelText="Upload from computer"
            accept={['.jpg', '.jpeg', '.png']}
          />
          <input type="hidden" name="avatar" bind:value={$form.avatar} />
        </div>

        {#if hideUploader}
          <Button on:click={handleChangeAvatar}>Change <EditOutline /></Button>
          <Button on:click={handleRemove}>Remove <TrashBinOutline /></Button>
        {/if}

        {#if shouldValidate && (fileNotUploaded || fileTooBig)}
          <div class="error-box">
            <div>{errorMsg}</div>
          </div>
        {/if}
      </div>
    </div>
  </Modal>
</div>
