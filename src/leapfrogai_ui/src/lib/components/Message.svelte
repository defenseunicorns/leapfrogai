<script lang="ts">
  import {page} from '$app/stores';
  import {Button, Card} from 'flowbite-svelte';
  import {Copy, Reset} from 'carbon-icons-svelte';
  import {type Message as VercelAIMessage} from '@ai-sdk/svelte';
  import markdownit from 'markdown-it';
  import hljs from 'highlight.js';
  import frog from '$assets/frog.png';
  import {writable} from 'svelte/store';
  import {EditOutline, UserCircleOutline} from 'flowbite-svelte-icons';
  import {twMerge} from 'tailwind-merge';
  import {threadsStore, toastStore} from '$stores';
  import {convertTextToMessageContentArr, getMessageText} from '$helpers/threads';
  import type {Message as OpenAIMessage} from 'openai/resources/beta/threads/messages';
  import {getAssistantImage, getCitations, handleMessageEdit, isRunAssistantMessage} from '$helpers/chatHelpers';
  import DynamicPictogram from '$components/DynamicPictogram.svelte';
  import type {AppendFunction} from '$lib/types/messages';
  import DOMPurify from 'isomorphic-dompurify';
  import TextareaV2 from '$components/LFTextArea.svelte';

  // TODO - text inside card should wrap, long messages are extending to right side
  // TODO - finish replacing carbon components and update buttons, left off at utility buttons
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
  class="whitespace-pre-line"
  role="toolbar"
  on:mouseover={() => (messageIsHovered = true)}
  on:mouseleave={() => (messageIsHovered = false)}
  on:focus={() => (messageIsHovered = true)}
  tabindex="0"
>
  <div class="flex flex-1 items-start">
    {#if message.role === 'user'}
      <div class="icon">
        <UserCircleOutline class="h-6 w-6" data-testid="user-icon" />
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

    <div class="flex flex-grow flex-col gap-1 overflow-hidden pb-1">
      {#if editMode}
        <TextareaV2
          data-testid="edit-message-input"
          {value}
          {onSubmit}
          class="mx-4 mt-[22px] resize-none bg-white dark:bg-gray-800"
        />
        <div class="flex justify-end gap-1">
          <Button size="sm" color="alternative" on:click={handleCancel}>Cancel</Button>
          <Button
            size="sm"
            disabled={$threadsStore.sendingBlocked}
            on:click={onSubmit}
            aria-label="submit edited message">Submit</Button
          >
        </div>
      {:else}
        <Card
          class={twMerge(
            'max-w-full break-all dark:bg-gray-700 dark:text-white',
            message.role === 'user' && 'bg-transparent shadow-none dark:bg-transparent'
          )}
        >
          <div class="flex flex-col gap-2">
            <div class="font-bold">
              {message.role === 'user' ? 'You' : getAssistantName(message.assistant_id)}
            </div>
            <!--eslint-disable-next-line svelte/no-at-html-tags -- We use DomPurity to sanitize the code snippet-->
            {@html md.render(DOMPurify.sanitize(getMessageText(message)))}
            <div class="flex flex-col items-start">
              {#each getCitations(message, $page.data.files) as { component: Component, props }}
                <svelte:component this={Component} {...props} />
              {/each}
            </div>
          </div>
        </Card>
      {/if}

      <div class="flex gap-1 pl-4">
        {#if message.role === 'user' && !editMode}
          <button
            data-testid="edit prompt btn"
            class={twMerge(
              'remove-btn-style',
              !messageIsHovered && 'hide',
              !$threadsStore.sendingBlocked && 'highlight-icon'
            )}
            on:click={() => (editMode = true)}
            aria-label="edit prompt"
            tabindex="0"><EditOutline /></button
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
            class={twMerge("remove-btn-style",  !messageIsHovered && 'hide', !$threadsStore.sendingBlocked && "highlight-icon")}

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
        .highlight-icon :global(svg) {
                cursor: pointer;
                fill: #c6c6c6;
                transition: fill 70ms ease;
                &:hover {
                fill: #f4f4f4;
                }
                }



</style>