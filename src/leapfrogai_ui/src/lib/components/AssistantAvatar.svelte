<script lang="ts">
  import Pictograms from '$components/Pictograms.svelte';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { AVATAR_FILE_SIZE_ERROR_TEXT, MAX_AVATAR_SIZE, NO_FILE_ERROR_TEXT } from '$lib/constants';
  import { Avatar, Button, Modal, P, TableSearch } from 'flowbite-svelte';
  import { twMerge } from 'tailwind-merge';
  import { EditOutline, TrashBinOutline } from 'flowbite-svelte-icons';
  import Fuse, { type FuseResult, type IFuseOptions } from 'fuse.js';
  import { iconMap } from '$constants/iconMap';
  import LFRadio from '$components/LFRadio.svelte';
  import FileUploaderButton from '$components/FileUploaderButton.svelte';

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
  let searchText = '';
  let searchResults: FuseResult<(keyof typeof iconMap)[]>[];
  let filteredPictograms: (keyof typeof iconMap)[] = [];

  const pictogramNames = Object.keys(iconMap);
  const options: IFuseOptions<unknown> = {
    minMatchCharLength: 3,
    shouldSort: false,
    findAllMatches: true,
    threshold: 0, // perfect matches only
    ignoreLocation: true
  };

  $: avatarToShow = tempFiles?.length > 0 ? URL.createObjectURL(tempFiles[0]) : $form.avatar;
  $: fileNotUploaded = !tempFiles[0]; // if on upload tab, you must upload a file to enable save
  $: fileTooBig = tempFiles[0]?.size > MAX_AVATAR_SIZE;
  $: hideUploader = avatarToShow ? true : tempFiles.length > 0;

  $: if (searchText) {
    const fuse = new Fuse(pictogramNames, options);
    searchResults = fuse.search(searchText);
    filteredPictograms = searchResults.map(
      (result) => result.item
    ) as unknown as (keyof typeof iconMap)[];
  }

  const handleRemove = (e) => {
    e.stopPropagation();
    tempFiles = [];
    $form.avatar = '';
    tempPictogram = selectedPictogramName || 'default';
    shouldValidate = false;
  };

  const handleClose = (e) => {
    e.stopPropagation();
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

  const handleChangeAvatar = (e) => {
    e.stopPropagation();
    fileUploaderRef.click(); // re-open upload dialog
  };

  const handleSubmit = (e) => {
    e.stopPropagation();

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
      <Avatar src={avatarToShow} size="lg" />
    {:else}
      <DynamicPictogram iconName={tempPictogram} size="md" class="text-white" />
    {/if}
  </button>
  <Modal bind:open={modalOpen} autoclose title="Avatar Image">
    <div id="parent-flexbox" class="flex h-full flex-col gap-4">
      <div id="child-flexbox-header" class="p-2">
        <div class="flex flex-col gap-2">
          <div class="flex gap-2">
            <LFRadio
              name="Pictogram"
              checked={selectedRadioButton === 'pictogram'}
              on:click={() => (selectedRadioButton = 'pictogram')}
              class="dark:text-gray-400">Pictogram</LFRadio
            >
            <LFRadio
              name="Upload"
              checked={selectedRadioButton === 'upload'}
              on:click={() => (selectedRadioButton = 'upload')}
              class="dark:text-gray-400">Upload</LFRadio
            >
          </div>
          <div class={selectedRadioButton === 'upload' && 'hidden'}>
            <TableSearch
              placeholder="Search"
              hoverable={true}
              bind:inputValue={searchText}
              innerDivClass="px-0"
              divClass="relative overflow-x-auto"
            />
          </div>
        </div>
      </div>
      <div id="child-flexbox-main" class="flex-1 overflow-y-auto p-2">
        <div
          id="pictograms"
          class={twMerge(
            selectedRadioButton === 'upload' && 'hidden',
            'flex-1  flex-col overflow-y-auto'
          )}
        >
          <Pictograms
            pictograms={filteredPictograms.length > 0 ? filteredPictograms : pictogramNames}
            bind:selectedPictogramName={tempPictogram}
          />
        </div>

        <div
          id="upload-components"
          class={twMerge('flex flex-col gap-2', selectedRadioButton === 'pictogram' && 'hidden')}
        >
          {#if avatarToShow}
            <Avatar src={avatarToShow} size="xl" />
          {/if}

          <div class={twMerge('flex flex-col gap-2', hideUploader && 'hidden')}>
            <P color="text-gray-400">Upload image</P>
            <P size="sm" color="text-gray-500">Supported file types are .jpg and .png.</P>
            <FileUploaderButton
              bind:ref={fileUploaderRef}
              bind:files={tempFiles}
              name="avatarFile"
              kind="tertiary"
              labelText="Upload from computer"
              accept={['.jpg', '.jpeg', '.png']}
              class="w-1/2"
            />
            <input type="hidden" name="avatar" bind:value={$form.avatar} />
          </div>

          {#if hideUploader}
            <div>
              <Button on:click={handleChangeAvatar}>Change <EditOutline /></Button>
              <Button on:click={handleRemove}>Remove <TrashBinOutline /></Button>
            </div>
          {/if}

          {#if shouldValidate && (fileNotUploaded || fileTooBig)}
            <div class="error-box">
              <div>{errorMsg}</div>
            </div>
          {/if}
        </div>
      </div>

      <div id="child-flexbox-footer" class="flex justify-center">
        <Button color="red" class="me-2" on:click={handleClose}>Cancel</Button>
        <Button on:click={handleSubmit}>Save</Button>
      </div>
    </div>
  </Modal>
</div>
