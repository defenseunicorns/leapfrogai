<script lang="ts">
  import { User, Upload, Edit, TrashCan } from 'carbon-icons-svelte';
  import {
    Button,
    FileUploader,
    FileUploaderButton,
    Modal,
    Tab,
    TabContent,
    Tabs
  } from 'carbon-components-svelte';

  let modalOpen = false;

  let files: File[];
  let imagePreviewUrl: string;
  let hideUploader = false;
</script>

<button
  class="user-icon remove-btn-style"
  tabindex="0"
  on:click|preventDefault={() => (modalOpen = true)}
>
  <User />
</button>

<Modal
  bind:open={modalOpen}
  modalHeading="Avatar Image"
  primaryButtonText="Save"
  secondaryButtonText="Cancel"
  on:click:button--secondary={() => (modalOpen = false)}
>
  <Tabs>
    <Tab label="Pictogram" />
    <Tab label="Upload" />
    <svelte:fragment slot="content">
      <TabContent>a</TabContent>
      <TabContent>
        <div class="avatar-upload-container">
          {#if imagePreviewUrl}<img src={imagePreviewUrl} class="avatar" />{/if}
          {#if !hideUploader}
            <FileUploader
              bind:files
              kind="tertiary"
              labelTitle="Upload image"
              buttonLabel="Upload from computer"
              labelDescription="Supported file types are .jpg and .png."
              accept={['.jpg', '.jpeg', '.png']}
              on:change={(e) => {
                hideUploader = true;
                imagePreviewUrl = URL.createObjectURL(e.detail[0]);
              }}
            />{/if}
          {#if hideUploader}
            <div class="edit-btns">
              <Button size="small" kind="tertiary" icon={Edit}>Change</Button>
              <Button size="small" kind="tertiary" icon={TrashCan}>Remove</Button>
            </div>
          {/if}
        </div>
      </TabContent>
    </svelte:fragment>
  </Tabs>
</Modal>

<style lang="scss">
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

  .heading {
    @include type.type-style('heading-compact-01');
  }
  .sub-heading {
    @include type.type-style('body-compact-01');
    color: themes.$text-secondary;
  }

  .avatar {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 12rem;
    height: 12rem;
    border-radius: 50%;
    padding: 0.5rem;
  }

  .avatar-upload-container{
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-03;
  }

  .edit-btns {
    display: flex;
    gap: layout.$spacing-03;
  }
</style>
