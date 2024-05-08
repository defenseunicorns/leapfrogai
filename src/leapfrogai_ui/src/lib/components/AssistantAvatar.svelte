<script lang="ts">
  import { Edit, TrashCan, User } from 'carbon-icons-svelte';
  import {
    Button,
    FileUploaderButton,
    Modal,
    RadioButton,
    RadioButtonGroup,
    Tab,
    TabContent,
    Tabs
  } from 'carbon-components-svelte';
  import Pictograms from '$components/Pictograms.svelte';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';

  export let files: File[];
  export let selectedPictogramName: string;

  let tempFiles: File[] = [];
  let modalOpen = false;
  let fileUploaderRef: HTMLInputElement;
  let selectedRadioButton: 'upload' | 'pictogram' = 'pictogram';

  $: hideUploader = tempFiles.length > 0;

  const handleRemove = () => {
    tempFiles = [];
    selectedPictogramName = '';
  };

  const handleChangeAvatar = () => {
    fileUploaderRef.click(); // re-open upload dialog
  };

  const handleCancel = () => {
    modalOpen = false;
    if (files?.length > 0) {
      tempFiles = [...files]; // reset to original file
    } else {
      tempFiles = [];
    }
  };

  $: console.log(selectedRadioButton);

  $: tempImagePreviewUrl = tempFiles?.length > 0 ? URL.createObjectURL(tempFiles[0]) : '';
  $: savedImagePreviewUrl = files?.length > 0 ? URL.createObjectURL(files[0]) : '';
</script>

<div class="container">
  <button
    class="user-icon remove-btn-style"
    tabindex="0"
    on:click|preventDefault={() => (modalOpen = true)}
  >
    {#if savedImagePreviewUrl}
      <div class="mini-avatar" style={`background-image: url(${savedImagePreviewUrl});`} />
    {:else}
      <DynamicPictogram iconName={selectedPictogramName} />
    {/if}
  </button>

  <Modal
    bind:open={modalOpen}
    modalHeading="Avatar Image"
    primaryButtonText="Save"
    secondaryButtonText="Cancel"
    on:close={() => {
      handleCancel();
    }}
    on:click:button--secondary={() => {
      handleCancel();
    }}
    on:submit={() => {
      files = [...tempFiles];
      modalOpen = false;
    }}
    style="--modal-height:{selectedRadioButton === 'pictogram' ? '100%' : 'auto'};"
  >
    <RadioButtonGroup bind:selected={selectedRadioButton}>
      <RadioButton labelText="Pictogram" value="pictogram" />
      <RadioButton labelText="Upload" value="upload" />
    </RadioButtonGroup>
    {#if selectedRadioButton === 'pictogram'}
      <Pictograms bind:selectedPictogramName />
    {:else}
      <div class="avatar-upload-container">
        {#if tempImagePreviewUrl}
          <div class="avatar" style={`background-image: url(${tempImagePreviewUrl});`} />
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
    :global(.bx--tab-content) {
      height: calc(100% - 3rem); // 3 rem is default modal margin-bottom, prevents extra scrollbar
    }
  }

  .user-icon :global(svg) {
    width: 3rem;
    height: 3rem;
    padding: layout.$spacing-03;
    border-radius: 50%;
    background-color: themes.$layer-01;
    transition: background-color 70ms ease;
    &:hover {
      background-color: themes.$layer-02;
    }
  }

  .avatar {
    width: 12rem;
    height: 12rem;
    border-radius: 50%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }

  .mini-avatar {
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }

  .avatar-upload-container {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-03;
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
</style>
