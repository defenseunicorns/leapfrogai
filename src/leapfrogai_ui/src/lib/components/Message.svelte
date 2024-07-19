<script lang="ts">
  import { page } from '$app/stores';
  import { Button, Tile } from 'carbon-components-svelte';
  import { Copy, Edit, Reset, UserAvatar } from 'carbon-icons-svelte';
  import { type Message as VercelAIMessage } from '@ai-sdk/svelte';
  import markdownit from 'markdown-it';
  import hljs from 'highlight.js';
  import { LFTextArea } from '$components';
  import frog from '$assets/frog.png';
  import { writable } from 'svelte/store';
  import { threadsStore, toastStore } from '$stores';
  import { convertTextToMessageContentArr, getMessageText } from '$helpers/threads';
  import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';
  import {
    getAssistantImage,
    getCitations,
    handleMessageEdit,
    isRunAssistantMessage
  } from '$helpers/chatHelpers';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import type { AppendFunction } from '$lib/types/messages';
  import DOMPurify from 'isomorphic-dompurify';

  export let message: OpenAIMessage;
  export let messages: OpenAIMessage[] = [];
  export let streamedMessages: VercelAIMessage[] = [];
  export let setMessages: ((messages: VercelAIMessage[]) => void) | undefined = undefined;
  export let isLastMessage: boolean;
  export let append: AppendFunction | undefined = undefined;

  // used for code formatting and handling
  const md = markdownit({
    highlight: function (str: string, language: string) {
      let code: string;
      if (language && hljs.getLanguage(language)) {
        try {
          code = md.utils.escapeHtml(hljs.highlight(str, { language }).value);
        } catch (__) {
          code = md.utils.escapeHtml(str);
        }
      } else {
        code = md.utils.escapeHtml(str);
      }

      return `<pre><code><code-block code="${code}" language="${language}"></code></pre>`;
    }
  });

  let assistantImage = isRunAssistantMessage(message)
    ? getAssistantImage($page.data.assistants || [], message.assistant_id!)
    : null;

  let messageIsHovered = false;
  let editMode = false;
  let value = writable<string>(getMessageText(message));

  const getAssistantName = (id?: string) => {
    if (!id) return 'LeapfrogAI Bot';
    return (
      $page.data.assistants?.find((assistant) => assistant.id === id)?.name || 'LeapfrogAI Bot'
    );
  };

  const onSubmit = async (e: SubmitEvent | KeyboardEvent | MouseEvent) => {
    e.preventDefault();
    editMode = false;

    await handleMessageEdit({
      messages,
      streamedMessages,
      message: { ...message, content: convertTextToMessageContentArr($value) },
      setMessages: setMessages!,
      append: append!,
      selectedAssistantId: $threadsStore.selectedAssistantId
    });
  };

  const handleCancel = () => {
    editMode = false;
    value.set(getMessageText(message)); // restore original value
  };

  const handleCopy = async (e) => {
    e.preventDefault();
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
        <UserAvatar style="width: 24px; height: 24px;" data-testid="user-icon" />
      </div>
    {:else if assistantImage && assistantImage.startsWith('http')}
      <img alt="Assistant" src={assistantImage} class="icon" data-testid="assistant-icon" />
    {:else if assistantImage}
      <div class="icon" data-testid="assistant-icon">
        <DynamicPictogram iconName={assistantImage} width="24px" height="24px" />
      </div>
    {:else}
      <img alt="LeapfrogAI" src={frog} class="icon" data-testid="leapfrog-icon" />
    {/if}

    <div class="message-and-utils">
      {#if editMode}
        <div class="edit-prompt">
          <LFTextArea {value} {onSubmit} ariaLabel="edit message input" />
          <div class="cancel-save">
            <Button size="small" kind="secondary" on:click={handleCancel}>Cancel</Button>
            <Button
              size="small"
              disabled={$threadsStore.sendingBlocked}
              on:click={onSubmit}
              aria-label="submit edited message">Submit</Button
            >
          </div>
        </div>
      {:else}
        <Tile style="line-height: 20px;">
          <div class="message-content">
            <div style="font-weight: bold">
              {message.role === 'user' ? 'You' : getAssistantName(message.assistant_id)}
            </div>
            <!--eslint-disable-next-line svelte/no-at-html-tags -- We use DomPurity to sanitize the code snippet-->
            {@html md.render(DOMPurify.sanitize(getMessageText(message)))}
            <div class="citations">
              {#each getCitations(message, $page.data.files) as { component: Component, props }}
                <svelte:component this={Component} {...props} />
              {/each}
            </div>
          </div>
        </Tile>
      {/if}

      <div class="utils">
        {#if message.role === 'user' && !editMode}
          <button
            data-testid="edit prompt btn"
            class="remove-btn-style"
            class:highlight-icon={!$threadsStore.sendingBlocked}
            class:hide={!messageIsHovered}
            on:click={() => (editMode = true)}
            aria-label="edit prompt"
            tabindex="0"><Edit /></button
          >
        {/if}
        {#if message.role !== 'user'}
          <button
            data-testid="copy btn"
            class="highlight-icon remove-btn-style"
            class:hide={!messageIsHovered}
            on:click={handleCopy}
            tabindex="0"
            aria-label="copy message"><Copy /></button
          >
        {/if}
        {#if message.role !== 'user' && isLastMessage && !$threadsStore.sendingBlocked}
          <button
            data-testid="regenerate btn"
            class="remove-btn-style"
            class:highlight-icon={!$threadsStore.sendingBlocked}
            class:hide={!messageIsHovered}
            on:click={async () =>
              await handleMessageEdit({
                messages,
                streamedMessages,
                message: messages[messages.length - 2],
                setMessages,
                append: append,
                selectedAssistantId: $threadsStore.selectedAssistantId
              })}
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
    gap: 0.25rem;
    overflow: hidden;
    padding-bottom: layout.$spacing-02;
  }

  .hide {
    opacity: 0;
    transition: opacity 0.2s;
  }
  .message {
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
    padding: 14px 0.25rem;
  }

  .cancel-save {
    display: flex;
    justify-content: flex-end;
    gap: 0.25rem;
    margin-top: 1px; // prevents text in editable text area from slightly jumping
  }

  .utils {
    display: flex;
    gap: 0.5rem;
    padding-left: 1rem;
  }

  .edit-prompt :global(.lf-text-area.bx--text-area) {
    background: #262626;
    outline: 1px solid #525252;
    border-bottom: 0;
    margin-top: 7px; // prevents edit box from jumping up on editMode
  }

  .message-content {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .citations {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
  }
</style>
