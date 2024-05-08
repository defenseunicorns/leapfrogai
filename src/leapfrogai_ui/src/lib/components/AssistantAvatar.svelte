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

  export let files: File[];
  export let selectedPictogramName: string;

  let tempFiles: File[] = [];
  let modalOpen = false;
  let fileUploaderRef: HTMLInputElement;
  let selectedRadioButton: 'upload' | 'pictogram' = 'pictogram';

  let hasClickedSave = false;
  $: invalid = selectedRadioButton === 'upload' && !tempFiles[0]; // if on upload tab, you must upload a file to click save
  let errorSubject = 'Please upload an image or select a pictogram';
  // TODO - file size validation

  $: hideUploader = tempFiles.length > 0;

  const handleRemove = () => {
    tempFiles = [];
    selectedPictogramName = '';
  };

  const handleChangeAvatar = () => {
    fileUploaderRef.click(); // re-open upload dialog
  };

  const handleCancel = () => {
    hasClickedSave = false;
    modalOpen = false;
    if (files?.length > 0) {
      tempFiles = [...files]; // reset to original file
    } else {
      tempFiles = [];
    }
  };

  $: tempImagePreviewUrl = tempFiles?.length > 0 ? URL.createObjectURL(tempFiles[0]) : '';
  $: savedImagePreviewUrl = files?.length > 0 ? URL.createObjectURL(files[0]) : '';
</script>

<div class="container">
  <button
    class="mini-avatar-container remove-btn-style"
    tabindex="0"
    on:click|preventDefault={() => (modalOpen = true)}
  >
    {#if savedImagePreviewUrl}
      <div class="mini-avatar-image" style={`background-image: url(${savedImagePreviewUrl});`} />
    {:else}
      <DynamicPictogram iconName={selectedPictogramName} width="32px" height="32px" />
    {/if}
  </button>

  <Modal
    bind:open={modalOpen}
    modalHeading="Avatar Image"
    shouldSubmitOnEnter={false}
    primaryButtonText="Save"
    secondaryButtonText="Cancel"
    on:close={() => {
      handleCancel();
    }}
    on:click:button--secondary={() => {
      handleCancel();
    }}
    on:submit={() => {
      hasClickedSave = true;
      if (!invalid) {
        files = [...tempFiles];
        modalOpen = false;
        hasClickedSave = false;
      }
    }}
    style="--modal-height:{selectedRadioButton === 'pictogram' ? '100%' : 'auto'};"
    class="avatar-modal"
  >
    <div class="avatar-modal">
      <RadioButtonGroup bind:selected={selectedRadioButton}>
        <RadioButton labelText="Pictogram" value="pictogram" />
        <RadioButton labelText="Upload" value="upload" />
      </RadioButtonGroup>
      {#if selectedRadioButton === 'pictogram'}
        <Pictograms bind:selectedPictogramName />
      {:else}
        <div class="avatar-upload-container">
          {#if tempImagePreviewUrl}
            <div class="avatar-container">
              <div class="avatar-image" style={`background-image: url(${tempImagePreviewUrl});`} />
            </div>
          {/if}

          <div class="image-uploader" style={hideUploader ? 'display: none' : 'display: block'}>
            <div class:bx--file--label={true}>Upload image</div>
            <div class:bx--label-description={true}>Supported file types are .jpg and .png.</div>
            <FileUploaderButton
              bind:ref={fileUploaderRef}
              bind:files={tempFiles}
              name="avatar"
              kind="tertiary"
              labelText="Upload from computer"
              accept={['.jpg', '.jpeg', '.png']}
            />
            {#if hasClickedSave && invalid && errorSubject}
              <div class="error-box">
                <div>{errorSubject}</div>
              </div>
            {/if}
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
        </div>
      {/if}
    </div>
  </Modal>
</div>

<style lang="scss">
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
