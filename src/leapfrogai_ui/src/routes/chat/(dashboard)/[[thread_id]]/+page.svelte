<script lang="ts">
  import { LFTextArea, PoweredByDU } from '$components';
  import { Button, Dropdown } from 'carbon-components-svelte';
  import { onMount, tick } from 'svelte';
  import { threadsStore, toastStore } from '$stores';
  import { ArrowRight, Checkmark, StopFilledAlt, UserProfile } from 'carbon-icons-svelte';
  import { type Message as VercelAIMessage, useAssistant, useChat } from '@ai-sdk/svelte';
  import { page } from '$app/stores';
  import { beforeNavigate, goto } from '$app/navigation';
  import Message from '$components/Message.svelte';
  import { getMessageText } from '$helpers/threads';
  import { getUnixSeconds } from '$helpers/dates.js';
  import { NO_SELECTED_ASSISTANT_ID } from '$constants';

  import {
    isRunAssistantResponse,
    resetMessages,
    saveMessage,
    stopThenSave
  } from '$helpers/chatHelpers';
  import {
    ERROR_GETTING_AI_RESPONSE_TEXT,
    ERROR_GETTING_ASSISTANT_MSG_TEXT,
    ERROR_SAVING_MSG_TEXT
  } from '$constants/toastMessages';

  export let data;

  /** LOCAL VARS **/
  let messageThreadDiv: HTMLDivElement;
  let lengthInvalid: boolean; // bound to child LFTextArea
  let assistantsList: Array<{ id: string; text: string }>;
  let hasSentAssistantMessage = false;
  /** END LOCAL VARS **/

  /** REACTIVE STATE **/
  $: $page.params.thread_id, threadsStore.setLastVisitedThreadId($page.params.thread_id);
  $: $page.params.thread_id,
    resetMessages({
      activeThread: data.thread,
      setChatMessages,
      setAssistantMessages,
      files: data.files
    });

  $: activeThreadMessages =
    $threadsStore.threads.find((thread) => thread.id === $page.params.thread_id)?.messages || [];
  $: messageStreaming = $isLoading || $status === 'in_progress';
  $: latestChatMessage = $chatMessages[$chatMessages.length - 1];
  $: latestAssistantMessage = $assistantMessages[$assistantMessages.length - 1];
  $: assistantMode =
    $threadsStore.selectedAssistantId !== NO_SELECTED_ASSISTANT_ID &&
    $threadsStore.selectedAssistantId !== 'manage-assistants';

  $: if (messageStreaming) threadsStore.setSendingBlocked(true);

  // Handle streaming chat completion messages
  $: if (isLoading)
    latestChatMessage?.role !== 'user' && threadsStore.setStreamingMessage(latestChatMessage);

  // Handle streaming assistant messages
  $: $assistantMessages, handleAssistantMessage();

  // assistant stream has completed
  $: $status, handleCompletedAssistantResponse();

  /** END REACTIVE STATE **/

  const handleAssistantMessage = async () => {
    if ($status === 'in_progress') {
      console.log('latest assistant msg', latestAssistantMessage);
      // The initial user message is stored with a short temp id by @ai-sdk/svelte, we need to wait for the
      // user message to be saved to the DB so we have the real id. Temp IDs appear to be 7 chars long, setting the
      // length check here higher for safety
      if (latestAssistantMessage?.role === 'user' && latestAssistantMessage.id.length > 15) {
        const userMessageId = $assistantMessages[$assistantMessages.length - 1].id;
        const messageRes = await fetch(
          `/api/messages?thread_id=${$page.params.thread_id}&message_id=${userMessageId}`
        );
        const message = await messageRes.json();
        await threadsStore.addMessageToStore(message);
      } else if (latestAssistantMessage?.role !== 'user') {
        // Streamed assistant responses don't contain an assistant_id, so we add it here
        // and also add a createdAt date if not present
        if (!latestAssistantMessage.assistant_id) {
          latestAssistantMessage.assistant_id = $threadsStore.selectedAssistantId;
        }

        if (!latestAssistantMessage.createdAt)
          latestAssistantMessage.createdAt =
            latestAssistantMessage.created_at || getUnixSeconds(new Date());

        threadsStore.setStreamingMessage(latestAssistantMessage);
        await threadsStore.setSendingBlocked(false);
      }
    }
  };

  const handleCompletedAssistantResponse = async () => {
    if (hasSentAssistantMessage && $status === 'awaiting_message') {
      const assistantResponseId = $assistantMessages[$assistantMessages.length - 1].id;
      const messageRes = await fetch(
        `/api/messages?thread_id=${$page.params.thread_id}&message_id=${assistantResponseId}`
      );
      const message = await messageRes.json();
      await threadsStore.addMessageToStore(message);
      threadsStore.setStreamingMessage(null);
    }
  };

  /** useChat - streams messages with the /api/chat route**/
  const {
    input: chatInput,
    handleSubmit: submitChatMessage,
    messages: chatMessages,
    setMessages: setChatMessages,
    isLoading,
    stop: chatStop,
    append: chatAppend,
    reload
  } = useChat({
    // Handle completed AI Responses
    onFinish: async (message: VercelAIMessage) => {
      try {
        if (data.thread?.id) {
          // Save with API to db
          const newMessage = await saveMessage({
            thread_id: data.thread.id,
            content: getMessageText(message),
            role: 'assistant'
          });

          await threadsStore.addMessageToStore(newMessage);
          threadsStore.setStreamingMessage(null);
        }
      } catch {
        toastStore.addToast({
          kind: 'error',
          title: 'Error',
          subtitle: 'Error saving AI Response'
        });
      }
      await threadsStore.setSendingBlocked(false);
    },
    onError: async () => {
      toastStore.addToast({
        kind: 'error',
        title: ERROR_GETTING_AI_RESPONSE_TEXT.title,
        subtitle: ERROR_GETTING_AI_RESPONSE_TEXT.subtitle
      });
      await threadsStore.setSendingBlocked(false);
    }
  });

  /** useAssistant - streams messages with the /api/chat/assistants route **/
  const {
    status,
    input: assistantInput,
    messages: assistantMessages,
    submitMessage: submitAssistantMessage,
    stop: assistantStop,
    setMessages: setAssistantMessages,
    append: assistantAppend
  } = useAssistant({
    api: '/api/chat/assistants',
    threadId: data.thread?.id,
    onError: async (e) => {
      // ignore this error b/c it is expected on cancel
      if (e.message !== 'BodyStreamBuffer was aborted') {
        toastStore.addToast({
          kind: 'error',
          title: ERROR_GETTING_ASSISTANT_MSG_TEXT.title,
          subtitle: ERROR_GETTING_ASSISTANT_MSG_TEXT.subtitle
        });
      }
      await threadsStore.setSendingBlocked(false);
    }
  });

  const sendAssistantMessage = async (e: SubmitEvent | KeyboardEvent) => {
    await threadsStore.setSendingBlocked(true);
    hasSentAssistantMessage = true;
    if (data.thread?.id) {
      // assistant mode
      $assistantInput = $chatInput;
      $chatInput = ''; // clear chat input

      await submitAssistantMessage(e, {
        // submit to AI (/api/chat/assistants)
        data: {
          message: $chatInput,
          assistantId: $threadsStore.selectedAssistantId,
          threadId: data.thread.id
        }
      });
      $assistantInput = '';
    }
    await threadsStore.setSendingBlocked(false);
  };

  const sendChatMessage = async (e: SubmitEvent | KeyboardEvent) => {
    await threadsStore.setSendingBlocked(true);
    if (data.thread?.id) {
      // Save with API
      try {
        const newMessage = await saveMessage({
          thread_id: data.thread.id,
          content: $chatInput,
          role: 'user'
        });
        // store user input
        await threadsStore.addMessageToStore(newMessage);
        submitChatMessage(e); // submit to AI (/api/chat)
      } catch {
        toastStore.addToast({
          kind: 'error',
          title: ERROR_SAVING_MSG_TEXT.title,
          subtitle: ERROR_SAVING_MSG_TEXT.subtitle
        });
        await threadsStore.setSendingBlocked(false);
      }
    }
  };

  // OpenAI returns the creation timestamp in seconds instead of milliseconds.
  // If a response comes in quickly, we need to delay 1 second to ensure the timestamps of the user message
  // and AI response are not exactly the same. This is important for sorting messages when they are initially loaded
  // from the db/API (ex. browser refresh). Streamed messages are sorted realtime and we modify the timestamps to
  // ensure we have millisecond precision.
  // setSendingBlocked (when called with the value 'false') automatically handles this delay
  const onSubmit = async (e: SubmitEvent | KeyboardEvent) => {
    e.preventDefault();
    if (($isLoading || $status === 'in_progress') && data.thread?.id) {
      const isAssistantChat = $status === 'in_progress';
      // message still sending
      await stopThenSave({
        activeThreadId: data.thread.id,
        messages: isAssistantChat ? $assistantMessages : $chatMessages,
        status: $status,
        isLoading: $isLoading || false,
        assistantStop,
        chatStop
      });
      await threadsStore.setSendingBlocked(false);
      return;
    } else {
      if (!data.thread?.id) {
        // create new thread
        await threadsStore.newThread($chatInput);
        await tick(); // allow store to update
      }
      if ($threadsStore.sendingBlocked) {
        toastStore.addToast({
          kind: 'warning',
          title: 'Rate limiting',
          subtitle: 'Please wait a moment before sending another message'
        });
        return;
      }
      assistantMode ? await sendAssistantMessage(e) : await sendChatMessage(e);
    }
  };

  onMount(async () => {
    assistantsList = [...(data.assistants || [])].map((assistant) => ({
      id: assistant.id,
      text: assistant.name || 'unknown'
    }));
    assistantsList.unshift({ id: NO_SELECTED_ASSISTANT_ID, text: 'Select assistant...' }); // add dropdown item for no assistant selected
    assistantsList.unshift({ id: `manage-assistants`, text: 'Manage assistants' }); // add dropdown item for manage assistants button
  });

  beforeNavigate(async () => {
    if (($isLoading || $status === 'in_progress') && data.thread?.id) {
      const isAssistantChat = $status === 'in_progress';
      await stopThenSave({
        activeThreadId: data.thread.id,
        messages: isAssistantChat ? $assistantMessages : $chatMessages,
        status: $status,
        isLoading: $isLoading || false,
        assistantStop,
        chatStop
      });
    }
  });
</script>

<div class="container">
  <form on:submit={onSubmit} class="container">
    <div class="messages-container">
      <div bind:this={messageThreadDiv}>
        {#each activeThreadMessages as message, index (message.id)}
          <Message
            messages={activeThreadMessages}
            streamedMessages={isRunAssistantResponse(message) ? $assistantMessages : $chatMessages}
            {message}
            isLastMessage={!$threadsStore.streamingMessage &&
              index === activeThreadMessages.length - 1}
            append={isRunAssistantResponse(message) ? assistantAppend : chatAppend}
            setMessages={isRunAssistantResponse(message) ? setAssistantMessages : setChatMessages}
          />
        {/each}
        {#if $threadsStore.streamingMessage}
          <Message
            messages={activeThreadMessages}
            streamedMessages={assistantMode ? $assistantMessages : $chatMessages}
            message={$threadsStore.streamingMessage}
            setMessages={assistantMode ? setAssistantMessages : setChatMessages}
            isLastMessage
            append={isRunAssistantResponse($threadsStore.streamingMessage)
              ? assistantAppend
              : chatAppend}
          />
        {/if}
      </div>
    </div>
    <hr id="divider" class="divider" />
    <div class:noAssistant={$threadsStore.selectedAssistantId === NO_SELECTED_ASSISTANT_ID}>
      <Dropdown
        data-testid="assistant-dropdown"
        disabled={$isLoading || $status === 'in_progress'}
        hideLabel
        direction="top"
        selectedId={$threadsStore.selectedAssistantId}
        on:select={async (e) => {
          if (e.detail.selectedId === 'manage-assistants') {
            await goto('/chat/assistants-management');
          } else {
            if ($threadsStore.selectedAssistantId === e.detail.selectedId)
              threadsStore.setSelectedAssistantId(NO_SELECTED_ASSISTANT_ID); //deselect
            else {
              threadsStore.setSelectedAssistantId(e.detail.selectedId);
            }
          }
        }}
        items={assistantsList}
        style="width: 25%; margin-bottom: 0.5rem"
        let:item
      >
        {#if item.id === `manage-assistants`}
          <button
            id="manage assistants"
            data-testid="assistants-management-btn"
            class="manage-assistants-btn remove-btn-style"
          >
            <UserProfile />
            {item.text}
          </button>
        {:else if item.id === NO_SELECTED_ASSISTANT_ID}
          <div class="noAssistant">
            {item.text}
          </div>
        {:else}
          <div class="assistant-dropdown-item">
            {item.text}
            {#if item.id !== NO_SELECTED_ASSISTANT_ID && $threadsStore.selectedAssistantId === item.id}
              <Checkmark data-testid="checked" />
            {/if}
          </div>
        {/if}
      </Dropdown>
    </div>
    <div class="chat-input">
      <LFTextArea
        value={chatInput}
        {onSubmit}
        ariaLabel="message input"
        placeholder="Type your message here..."
        bind:showLengthError={lengthInvalid}
      />

      {#if !$isLoading && $status !== 'in_progress'}
        <Button
          data-testid="send message"
          kind="secondary"
          icon={ArrowRight}
          size="field"
          type="submit"
          iconDescription="send"
          disabled={!$chatInput || lengthInvalid || $threadsStore.sendingBlocked}
        />
      {:else}
        <Button
          data-testid="cancel message"
          kind="secondary"
          size="field"
          type="submit"
          icon={StopFilledAlt}
          iconDescription="cancel"
        />
      {/if}
    </div>
    <PoweredByDU />
  </form>
</div>

<style lang="scss">
  .container {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .messages-container {
    display: flex;
    flex-direction: column-reverse;
    flex-grow: 1;
    overflow: auto;
    scrollbar-width: none;
  }

  .chat-input {
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    gap: 0.5rem;
  }

  .manage-assistants-btn {
    display: flex;
    align-items: center;
    gap: layout.$spacing-03;
  }

  .assistant-dropdown-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  :global(#manage-assistants) {
    z-index: 2; // ensures outline is on top of border of item below
    outline: 1px solid themes.$border-subtle-03;
    :global(.bx--list-box__menu_item__option) {
      padding-right: 0.25rem;
    }
  }

  .noAssistant {
    color: $gray-50;
    :global(.bx--list-box__label) {
      color: $gray-50;
    }
  }
</style>
