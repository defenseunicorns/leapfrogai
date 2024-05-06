<script lang="ts">
  import { Edit, TrashCan, User } from 'carbon-icons-svelte';
  import {
    Button,
    FileUploaderButton,
    Modal,
    Tab,
    TabContent,
    Tabs
  } from 'carbon-components-svelte';
  import Pictograms from '$components/Pictograms.svelte';

  let imagePreviewUrl: string;
  let modalOpen = false;
  let fileUploaderRef: HTMLInputElement;
  export let files: File[];
  let hideUploader = false;
  let selectedTab: number;

  let shouldRunOnClose = true;

  const clearInputFile = () => {
    files = [];
    imagePreviewUrl = '';
  };
  const handleRemove = () => {
    clearInputFile();
    hideUploader = false;
  };

  const handleChangeAvatar = () => {
    fileUploaderRef.click(); // re-open upload dialog
  };
</script>

<div class="container">
  <button
    class="user-icon remove-btn-style"
    tabindex="0"
    on:click|preventDefault={() => (modalOpen = true)}
  >
    {#if imagePreviewUrl}
      <img
        src={imagePreviewUrl}
        class="mini-avatar"
        alt="avatar"
        style={`background-image: url(${imagePreviewUrl});`}
      />
    {:else}
      <User />
    {/if}
  </button>

  <Modal
    bind:open={modalOpen}
    modalHeading="Avatar Image"
    primaryButtonText="Save"
    secondaryButtonText="Cancel"
    on:close={() => {
      if (shouldRunOnClose) {
        modalOpen = false;
        handleRemove();
      }
    }}
    on:click:button--secondary={() => {
      modalOpen = false;
      handleRemove();
    }}
    on:submit={() => {
      //on:close is also called when submit button clicked, override to not run that code, otherwise we would
      // lose the file
      shouldRunOnClose = false;
      modalOpen = false;
    }}
    style="--modal-height:{selectedTab === 0 ? '100%' : 'auto'};"
  >
    <Tabs bind:selected={selectedTab}>
      <Tab label="Pictogram" />
      <Tab label="Upload" />
      <svelte:fragment slot="content">
        <TabContent><Pictograms /></TabContent>
        <TabContent>
          <div class="avatar-upload-container">
            {#if imagePreviewUrl}
              <img
                src={imagePreviewUrl}
                class="avatar"
                alt="avatar"
                style={`background-image: url(${imagePreviewUrl});`}
              />
            {/if}

            <div class="image-uploader" style={hideUploader ? 'display: none' : 'display: block'}>
              <div class:bx--file--label={true}>Upload image</div>
              <div class:bx--label-description={true}>Supported file types are .jpg and .png.</div>
              <FileUploaderButton
                bind:ref={fileUploaderRef}
                bind:files
                name="avatar"
                kind="tertiary"
                labelText="Upload from computer"
                accept={['.jpg', '.jpeg', '.png']}
                on:change={(e) => {
                  hideUploader = true;
                  imagePreviewUrl = URL.createObjectURL(e.detail[0]);
                }}
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
        </TabContent>
      </svelte:fragment>
    </Tabs>
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
    object-fit: cover;
    background-position: center;
  }

  .mini-avatar {
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    object-fit: cover;
    background-position: center;
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
