<script lang="ts">
  import { Edit, TrashCan } from 'carbon-icons-svelte';
  import {
    Button,
    FileUploaderButton,
    Modal,
    RadioButton,
    RadioButtonGroup
  } from 'carbon-components-svelte';
  import Pictograms from '$components/Pictograms.svelte';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import { AVATAR_FILE_SIZE_ERROR_TEXT, MAX_AVATAR_SIZE, NO_FILE_ERROR_TEXT } from '$lib/constants';

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

<div class="container">
  <button
    class="mini-avatar-container remove-btn-style"
    tabindex="0"
    on:click|preventDefault={() => (modalOpen = true)}
    data-testid="mini-avatar-container"
  >
    {#if avatarToShow}
      <div class="mini-avatar-image" style={`background-image: url(${avatarToShow});`} />
    {:else}
      <DynamicPictogram iconName={tempPictogram} width="32px" height="32px" />
    {/if}
  </button>

  <Modal
    bind:open={modalOpen}
    modalHeading="Avatar Image"
    shouldSubmitOnEnter={false}
    primaryButtonText="Save"
    secondaryButtonText="Cancel"
    on:close={handleClose}
    on:click:button--secondary={handleClose}
    on:submit={handleSubmit}
    style="--modal-height:{tempPictogram === 'pictogram' ? '100%' : 'auto'};"
    class="avatar-modal"
  >
    <div class="avatar-modal">
      <RadioButtonGroup bind:selected={selectedRadioButton}>
        <RadioButton labelText="Pictogram" value="pictogram" />
        <RadioButton labelText="Upload" value="upload" />
      </RadioButtonGroup>
      <span class:hidden={selectedRadioButton === 'upload'} style="height: 100%;">
        <Pictograms bind:selectedPictogramName={tempPictogram} />
      </span>

      <div class="avatar-upload-container" class:hidden={selectedRadioButton === 'pictogram'}>
        {#if avatarToShow}
          <div class="avatar-container">
            <div
              data-testid="image-upload-avatar"
              class="avatar-image"
              style={`background-image: url(${avatarToShow});`}
            />
          </div>
        {/if}

        <div class="image-uploader" style={hideUploader ? 'display: none' : 'display: block'}>
          <div class:bx--file--label={true}>Upload image</div>
          <div class:bx--label-description={true}>Supported file types are .jpg and .png.</div>
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
          <div class="edit-btns">
            <Button size="small" kind="tertiary" icon={Edit} on:click={handleChangeAvatar}
              >Change</Button
            >
            <Button size="small" kind="tertiary" icon={TrashCan} on:click={handleRemove}
              >Remove</Button
            >
          </div>
        {/if}

        {#if shouldValidate && (fileNotUploaded || fileTooBig)}
          <div class="error-box">
            <div>{errorMsg}</div>
          </div>
        {/if}
      </div>
    </div></Modal
  >
</div>

<style lang="scss">
  .hidden {
    display: none !important;
  }

  .container {
    :global(.bx--modal-container) {
      height: var(
        --modal-height
      ); // keeps height fixed when searching pictograms, but not that size for avatar upload
      width: 80%;
    }
  }
  .avatar-upload-container {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-03;
  }

  .avatar-modal {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-05;
    height: calc(100% - 3rem); // 3 rem is default modal margin-bottom, prevents extra scrollbar
  }

  .mini-avatar-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    background-color: themes.$layer-active-03;
    transition: background-color 70ms ease;
    &:hover {
      background-color: themes.$layer-selected-hover-03;
    }
    .mini-avatar-image {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
    }
  }

  .avatar-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 12rem;
    height: 12rem;
    border-radius: 50%;
    background-color: themes.$layer-active-03;
    .avatar-image {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
    }
  }

  .image-uploader {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-03;
  }

  .edit-btns {
    display: flex;
    gap: layout.$spacing-03;
  }

  .error-box {
    border: 2px solid $red-30;
    color: $red-30;
    max-width: 20rem;
    padding: layout.$spacing-02;
    margin-top: layout.$spacing-05;
  }
</style>
