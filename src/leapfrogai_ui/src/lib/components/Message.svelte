<script lang="ts">
  import { page } from '$app/stores';
  import { Button, Card } from 'flowbite-svelte';
  import { type Message as VercelAIMessage } from '@ai-sdk/svelte';
  import markdownit from 'markdown-it';
  import hljs from 'highlight.js';
  import frog from '$assets/frog.png';
  import { writable } from 'svelte/store';
  import {
    EditOutline,
    FileCopyOutline,
    RedoOutline,
    UserCircleOutline
  } from 'flowbite-svelte-icons';
  import { twMerge } from 'tailwind-merge';
  import { assistantsStore, threadsStore, toastStore } from '$stores';
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
  import TextareaV2 from '$components/LFTextArea.svelte';
  import IconButton from '$components/IconButton.svelte';
  import MessagePendingSkeleton from '$components/MessagePendingSkeleton.svelte';
  import UploadedFileCard from '$components/UploadedFileCard.svelte';

  export let message: OpenAIMessage;
  export let messages: OpenAIMessage[] = [];
  export let streamedMessages: VercelAIMessage[] = [];
  export let setMessages: ((messages: VercelAIMessage[]) => void) | undefined = undefined;
  export let isLastMessage: boolean;
  export let append: AppendFunction | undefined = undefined;

  $: messageText = getMessageText(message);

  // used for code formatting and handling
  const md = markdownit({
    html: true,
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

      return `<pre><code><code-block code="${code}" language="${language}" /></code></pre>`;
    }
  });

  let assistantImage = isRunAssistantMessage(message)
    ? getAssistantImage($assistantsStore.assistants || [], message.assistant_id!)
    : null;

  let messageIsHovered = false;
  let editMode = false;
  let value = writable<string>(getMessageText(message));

  const getAssistantName = (id?: string) => {
    if (!id) return 'LeapfrogAI Bot';
    return (
      $assistantsStore.assistants?.find((assistant) => assistant.id === id)?.name ||
      'LeapfrogAI Bot'
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
      selectedAssistantId: $assistantsStore.selectedAssistantId
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

  $: fileMetadata = message.metadata?.filesMetadata
    ? JSON.parse(message.metadata.filesMetadata)
    : null;
</script>

<div
  data-testid="message"
  class="whitespace-pre-line"
  role="toolbar"
  on:mouseover={() => (messageIsHovered = true)}
  on:mouseleave={() => (messageIsHovered = false)}
  on:focus={() => (messageIsHovered = true)}
  tabindex="0"
>
  <div class="flex flex-1 items-start">
    {#if message.role === 'user'}
      <div class="chat-icon">
        <UserCircleOutline class="h-6 w-6" data-testid="user-icon" />
      </div>
    {:else if assistantImage && assistantImage.startsWith('http')}
      <img alt="Assistant" src={assistantImage} class="chat-icon" data-testid="assistant-icon" />
    {:else if assistantImage}
      <div class="chat-icon" data-testid="assistant-icon">
        <DynamicPictogram size="xs" iconName={assistantImage} />
      </div>
    {:else}
      <img alt="LeapfrogAI" src={frog} class="chat-icon" data-testid="leapfrogai-icon" />
    {/if}

    <div class="flex flex-grow flex-col gap-1 overflow-hidden pb-1">
      {#if editMode}
        <TextareaV2
          data-testid="edit-message-input"
          {value}
          {onSubmit}
          class="mx-4 mt-[54px] resize-none bg-white dark:bg-gray-800"
        />
        <div class="flex justify-end gap-1">
          <Button size="sm" color="alternative" on:click={handleCancel}>Cancel</Button>
          <Button
            size="sm"
            disabled={$threadsStore.sendingBlocked}
            on:click={onSubmit}
            aria-label="submit edited message"
            data-testid="submit-edit-message">Submit</Button
          >
        </div>
      {:else}
        <Card
          class={twMerge(
            'max-w-full break-words border-none dark:bg-gray-700 dark:text-white',
            message.role === 'user' && 'bg-transparent shadow-none dark:bg-transparent'
          )}
        >
          <div class="flex flex-col gap-2">
            <div class="font-bold">
              {message.role === 'user' ? 'You' : getAssistantName(message.assistant_id)}
            </div>
            {#if fileMetadata}
              <div id="uploaded-files" class={'flex max-w-full  gap-2 overflow-x-auto bg-gray-900'}>
                {#each fileMetadata as file}
                  <UploadedFileCard fileMetadata={file} disableDelete />
                {/each}
              </div>
            {/if}
            {#if message.role !== 'user' && !messageText}
              <MessagePendingSkeleton size="sm" class="mt-4" darkColor="bg-gray-500" />
            {:else}
              <div id="message-content-container">
                <!--eslint-disable-next-line svelte/no-at-html-tags -- We use DomPurity to sanitize the code snippet-->
                {@html DOMPurify.sanitize(md.render(messageText), {
                  CUSTOM_ELEMENT_HANDLING: {
                    tagNameCheck: /^code-block$/,
                    attributeNameCheck: /^(code|language)$/,
                    allowCustomizedBuiltInElements: false
                  }
                })}
              </div>
              <div class="flex flex-col items-start">
                {#each getCitations(message, $page.data.files) as { component: Component, props }}
                  <svelte:component this={Component} {...props} />
                {/each}
              </div>
            {/if}
          </div>
        </Card>
      {/if}

      <div class="flex gap-1 pl-4">
        {#if message.role === 'user' && !editMode && !message.metadata?.wasTranscriptionOrTranslation}
          <IconButton
            class={!messageIsHovered && 'hide'}
            on:click={() => (editMode = true)}
            aria-label="edit prompt"
            data-testid="edit-message"
            tabindex="0"
          >
            <EditOutline />
          </IconButton>
        {/if}
        {#if message.role !== 'user'}
          <IconButton
            data-testid="copy btn"
            class={!messageIsHovered && 'hide'}
            on:click={handleCopy}
            tabindex="0"
            aria-label="copy message"
          >
            <FileCopyOutline />
          </IconButton>
        {/if}
        {#if message.role !== 'user' && isLastMessage && !$threadsStore.sendingBlocked && !message.metadata?.wasTranscriptionOrTranslation}
          <IconButton
            data-testid="regenerate btn"
            class={!messageIsHovered && 'hide'}
            disabled={$threadsStore.sendingBlocked}
            on:click={async () =>
              await handleMessageEdit({
                messages,
                streamedMessages,
                message: messages[messages.length - 2],
                setMessages,
                append: append,
                selectedAssistantId: $assistantsStore.selectedAssistantId
              })}
            aria-label="regenerate message"
            tabindex="0"
          >
            <RedoOutline />
          </IconButton>
        {/if}
      </div>
    </div>
  </div>
</div>
