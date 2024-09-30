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

  export let form;

  let originalAvatar = $form.avatar;
  let selectedPictogramName = $form.pictogram || 'default';
  let tempPictogram = selectedPictogramName;
  let modalOpen = false;
  let selectedRadioButton: 'upload' | 'pictogram' = originalAvatar ? 'upload' : 'pictogram';
  let shouldValidate = false;
  let fileUploaderRef: HTMLInputElement;
  let errorMsg = '';
  let searchText = '';
  let searchResults: FuseResult<(keyof typeof iconMap)[]>[];
  let filteredPictograms: (keyof typeof iconMap)[] = [];
  let skipCloseActions = false;

  const pictogramNames = Object.keys(iconMap);
  const options: IFuseOptions<unknown> = {
    minMatchCharLength: 3,
    shouldSort: false,
    findAllMatches: true,
    threshold: 0, // perfect matches only
    ignoreLocation: true
  };

  $: fileNotUploaded = !$form.avatar && !$form.avatarFile; // if on upload tab, you must upload a file to enable save
  $: avatarToShow = $form.avatarFile ? URL.createObjectURL($form.avatarFile) : $form.avatar;

  $: fileTooBig = $form.avatarFile?.size > MAX_AVATAR_SIZE;
  $: hideUploader = avatarToShow ? true : $form.avatarFile;

  $: if (searchText) {
    const fuse = new Fuse(pictogramNames, options);
    searchResults = fuse.search(searchText);
    filteredPictograms = searchResults.map(
      (result) => result.item
    ) as unknown as (keyof typeof iconMap)[];
  }

  const handleRemove = (e) => {
    e.stopPropagation();
    clearFileInput();
    $form.avatar = '';
    tempPictogram = selectedPictogramName;
    shouldValidate = false;
  };

  const handleCancel = (e) => {
    e.stopPropagation();

    // clicking on save will trigger this function via on:close for modal
    // if submitting, this block should not run, only when cancelling should it run
    if (!skipCloseActions) {
      shouldValidate = false;
      modalOpen = false;
      $form.avatar = originalAvatar;
      tempPictogram = selectedPictogramName; // reset to original pictogram
      if (!$form.avatar) {
        clearFileInput();
      }
      fileUploaderRef.value = ''; // Reset the file input value to ensure input event detection
    }
    skipCloseActions = false;
  };

  const handleChangeAvatar = (e) => {
    e.stopPropagation();
    fileUploaderRef.click(); // re-open upload dialog
  };

  const clearFileInput = () => {
    fileUploaderRef.value = '';
    $form.avatarFile = null;
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
    } else {
      // pictogram tab
      selectedPictogramName = tempPictogram;
      $form.pictogram = tempPictogram;
      $form.avatar = ''; // remove saved avatar
      clearFileInput();
    }

    modalOpen = false;
    shouldValidate = false;
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
  <Modal
    bind:open={modalOpen}
    autoclose
    title="Avatar Image"
    on:close={handleCancel}
    color="primary"
  >
    <div id="parent-flexbox" class="flex h-full flex-col gap-4">
      <div id="child-flexbox-header" class="p-2">
        <div class="flex flex-col gap-2">
          <div class="flex gap-2">
            <LFRadio
              data-testid="pictogram-radio-btn"
              name="Pictogram"
              checked={selectedRadioButton === 'pictogram'}
              on:click={() => (selectedRadioButton = 'pictogram')}
              class="dark:text-gray-400">Pictogram</LFRadio
            >
            <LFRadio
              data-testid="upload-radio-btn"
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
            <Avatar src={avatarToShow} size="xl" data-testid="image-upload-avatar" />
          {/if}

          <div class={twMerge('flex flex-col gap-2', hideUploader && 'hidden')}>
            <P>Upload image</P>
            <P size="sm" color="dark:text-gray-400">Supported file types are .jpg and .png.</P>
            <Button
              on:click={(e) => {
                e.stopPropagation();
                fileUploaderRef?.click();
              }}
              tabindex={0}
              class="w-1/2"
            >
              Upload from computer
            </Button>
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
        <Button color="alternative" class="me-2" on:click={handleCancel}>Cancel</Button>
        <Button on:click={handleSubmit}>Save</Button>
      </div>
    </div>
  </Modal>
  <!--    Important! These inputs must be outside of the modal or the image will be lost when the modal closes
  The hidden inputs will not be nested inside the parent <form> if they are included inside the modal
  -->
  <input
    bind:this={fileUploaderRef}
    on:input={(e) => {
      const file = e.currentTarget.files[0];
      $form.avatarFile = file ?? null;
    }}
    multiple={false}
    type="file"
    tabindex="-1"
    accept={['.jpg', '.jpeg', '.png']}
    name="avatarFile"
    class="sr-only"
  />
  <input type="hidden" name="avatar" bind:value={$form.avatar} />
  <input type="hidden" name="pictogram" bind:value={selectedPictogramName} />
</div>
