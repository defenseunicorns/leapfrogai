<script lang="ts">
  import { Button, Tile } from 'carbon-components-svelte';
  import { Copy, Edit, Reset, UserAvatar } from 'carbon-icons-svelte';
  import { type Message as AIMessage } from 'ai/svelte';
  import { LFTextArea } from '$components';
  import frog from '$assets/frog.png';
  import { writable } from 'svelte/store';
  import { toastStore } from '$stores';
  import { getMessageText } from '$helpers/threads';

  export let handleMessageEdit: (
    event: SubmitEvent | KeyboardEvent | MouseEvent,
    message: AIMessage
  ) => Promise<void>;
  export let handleRegenerate: () => Promise<void>;
  export let message: AIMessage;
  export let isLastMessage: boolean;
  export let isLoading: boolean;

  let messageIsHovered = false;
  let editMode = false;
  let value = writable(getMessageText(message));

  const onSubmit = async (e: SubmitEvent | KeyboardEvent | MouseEvent) => {
    editMode = false;
    await handleMessageEdit(e, { ...message, content: $value });
  };

  const handleCancel = () => {
    editMode = false;
    value.set(getMessageText(message)); // restore original value
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText($value);
      toastStore.addToast({
        kind: 'info',
        title: 'Response Copied',
        subtitle: `Response message copied.`
      });
    } catch {
      toastStore.addToast({
        kind: 'error',
        title: 'Error',
        subtitle: `Error copying text.`
      });
    }
  };
</script>

<div
  data-testid="message"
  class="message"
  role="toolbar"
  class:transparent={message.role === 'user'}
  on:mouseover={() => (messageIsHovered = true)}
  on:mouseleave={() => (messageIsHovered = false)}
  on:focus={() => (messageIsHovered = true)}
  tabindex="0"
>
  <div class="message-and-avatar">
    {#if message.role === 'user'}
      <div class="icon">
        <UserAvatar style="width: 24px; height: 24px;" />
      </div>
    {:else}
      <img alt="LeapfrogAI" src={frog} class="icon" />
    {/if}

    <div class="message-and-utils">
      {#if editMode}
        <div class="edit-prompt">
          <LFTextArea {value} {onSubmit} ariaLabel="edit message input" />
          <div class="cancel-save">
            <Button size="small" kind="secondary" on:click={handleCancel}>Cancel</Button>
            <Button
              size="small"
              disabled={isLoading}
              on:click={onSubmit}
              aria-label="submit edited message">Submit</Button
            >
          </div>
        </div>
      {:else}
        <Tile style="line-height: 20px;">{getMessageText(message)}</Tile>
      {/if}

      <div class="utils">
        {#if message.role === 'user' && !editMode}
          <button
            data-testid="edit prompt btn"
            class="highlight-icon remove-btn-style"
            class:hide={!messageIsHovered}
            on:click={() => (editMode = true)}
            aria-label="edit prompt"
            tabindex="0"><Edit /></button
          >
        {/if}
        {#if message.role !== 'user' && (isLastMessage ? !isLoading : true)}
          <button
            data-testid="copy btn"
            class="highlight-icon remove-btn-style"
            class:hide={!messageIsHovered}
            on:click={handleCopy}
            tabindex="0"
            aria-label="copy message"><Copy /></button
          >
        {/if}
        {#if message.role !== 'user' && isLastMessage && !isLoading}
          <button
            data-testid="regenerate btn"
            class="highlight-icon remove-btn-style"
            class:hide={!messageIsHovered}
            on:click={handleRegenerate}
            aria-label="regenerate message"
            tabindex="0"><Reset /></button
          >
        {/if}
      </div>
    </div>
  </div>
</div>

<style lang="scss">
  .message-and-avatar {
    display: flex;
    flex: 1;
    align-items: flex-start;
  }

  .message-and-utils {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: layout.$spacing-02;
  }

  .hide {
    opacity: 0;
    transition: opacity 0.2s;
  }
  .message {
    display: flex;
    white-space: pre-line;
  }

  .transparent {
    :global(.bx--tile) {
      background-color: transparent;
    }
  }
  .icon {
    width: 32px;
    height: 52px;
    padding: 14px layout.$spacing-02;
  }

  .cancel-save {
    display: flex;
    justify-content: flex-end;
    gap: layout.$spacing-02;
    margin-top: 1px; // prevents text in editable text area from slightly jumping
  }

  .utils {
    display: flex;
    gap: layout.$spacing-03;
    padding-left: layout.$spacing-05;
  }

  .highlight-icon :global(svg) {
    cursor: pointer;
    fill: themes.$icon-secondary;
    transition: fill 70ms ease;
    &:hover {
      fill: themes.$icon-primary;
    }
  }

  .edit-prompt :global(.lf-text-area.bx--text-area) {
    background: themes.$background;
    outline: 1px solid themes.$layer-02;
    border-bottom: 0;
    margin-top: 7px; // prevents edit box from jumping up on editMode
  }
</style>
