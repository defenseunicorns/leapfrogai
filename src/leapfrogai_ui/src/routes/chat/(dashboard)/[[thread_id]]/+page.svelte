<script lang="ts">
  import { LFTextArea, PoweredByDU } from '$components';
  import { Button, Dropdown } from 'carbon-components-svelte';
  import { afterUpdate, onMount, tick } from 'svelte';
  import { threadsStore, toastStore } from '$stores';
  import { ArrowRight, Checkmark, StopFilledAlt, UserProfile } from 'carbon-icons-svelte';
  import { type Message as VercelAIMessage, useAssistant, useChat } from 'ai/svelte';
  import { page } from '$app/stores';
  import { beforeNavigate, goto } from '$app/navigation';
  import Message from '$components/Message.svelte';
  import { getMessageText } from '$helpers/threads';
  import { getUnixSeconds } from '$helpers/dates.js';
  import { NO_SELECTED_ASSISTANT_ID } from '$constants';

  import {
    isRunAssistantResponse,
    processAnnotations,
    resetMessages,
    saveMessage,
    sortMessages,
    stopThenSave
  } from '$helpers/chatHelpers';
  import {
    ERROR_GETTING_AI_RESPONSE_TEXT,
    ERROR_GETTING_ASSISTANT_MSG_TEXT,
    ERROR_SAVING_MSG_TEXT
  } from '$constants/toastMessages';

  import { convertMessageToVercelAiMessage } from '$helpers/threads.js';

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

  $: assistantMode =
    $threadsStore.selectedAssistantId !== NO_SELECTED_ASSISTANT_ID &&
    $threadsStore.selectedAssistantId !== 'manage-assistants';

  $: if ($isLoading || $status === 'in_progress') threadsStore.setSendingBlocked(true);

  // new streamed assistant message received (add in assistant_id and ensure it has a created_at timestamp)
  $: $assistantMessages, modifyStreamedAssistantResponse();

  // assistant stream has completed
  $: if (hasSentAssistantMessage && $status === 'awaiting_message') {
    fetchAndParseCompletedAssistantResponse();
  }

  $: sortedMessages = sortMessages([...$chatMessages, ...$assistantMessages]);

  /** END REACTIVE STATE **/

  // Annotations are stored after the run completes, so we re-fetch the last message to get them
  const fetchAndParseCompletedAssistantResponse = async () => {
    try {
      const messageRes = await fetch(
        `/api/messages?thread_id=${$page.params.thread_id}&message_id=${$assistantMessages[$assistantMessages.length - 1].id}`
      );
      const message = await messageRes.json();
      const parsedMessage = processAnnotations(message, data.files);
      const assistantMessagesCopy = [...$assistantMessages];
      assistantMessagesCopy[assistantMessagesCopy.length - 1] =
        convertMessageToVercelAiMessage(parsedMessage);
      setAssistantMessages(assistantMessagesCopy);
      threadsStore.updateMessage(
        $page.params.thread_id,
        $assistantMessages[$assistantMessages.length - 1].id,
        parsedMessage
      );
    } catch {
      // Fail Silently - error notification would not be useful to user, on failure, just show unparsed message
    }
  };

  const modifyStreamedAssistantResponse = async () => {
    // Streamed assistant responses don't contain an assistant_id, so we add it here
    // and also add a createdAt date if not present
    const assistantMessagesCopy = [...$assistantMessages];
    const latestMessage = assistantMessagesCopy[assistantMessagesCopy.length - 1];
    if (latestMessage) {
      if (!latestMessage.assistant_id) {
        latestMessage.assistant_id = $threadsStore.selectedAssistantId;
      }

      if (!latestMessage.createdAt)
        latestMessage.createdAt = latestMessage.created_at || getUnixSeconds(new Date());

      setAssistantMessages(assistantMessagesCopy);
    }
    await threadsStore.setSendingBlocked(false);
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
        if (!assistantMode && data.thread?.id) {
          // Save with API to db
          const newMessage = await saveMessage({
            thread_id: data.thread.id,
            content: getMessageText(message),
            role: 'assistant'
          });

          await threadsStore.addMessageToStore(newMessage);
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
    hasSentAssistantMessage = true;
    await threadsStore.setSendingBlocked(true);
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

  afterUpdate(() => {
    // Scroll to bottom
    messageThreadDiv.scrollTop = messageThreadDiv.scrollHeight;
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

<div class="chat-inner-content">
  <div class="messages" bind:this={messageThreadDiv}>
    {#each sortedMessages as message, index (message.id)}
      <Message
        allStreamedMessages={sortedMessages}
        {message}
        messages={isRunAssistantResponse(message) ? $assistantMessages : $chatMessages}
        setMessages={isRunAssistantResponse(message) ? setAssistantMessages : setChatMessages}
        isLastMessage={index === sortedMessages.length - 1}
        append={isRunAssistantResponse(message) ? assistantAppend : chatAppend}
        {reload}
      />
    {/each}
  </div>

  <hr id="divider" class="divider" />
  <div
    class="chat-form-container"
    class:noAssistant={$threadsStore.selectedAssistantId === NO_SELECTED_ASSISTANT_ID}
  >
    <form on:submit={onSubmit}>
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
    </form>
    <PoweredByDU />
  </div>
</div>

<style lang="scss">
  .chat-inner-content {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    height: 100%;
  }

  .messages {
    display: flex;
    flex-direction: column;
    gap: layout.$spacing-03;
    margin-bottom: layout.$spacing-05;
    overflow: scroll;
    scrollbar-width: none;
    padding: 0rem layout.$spacing-05;
  }

  .chat-form-container {
    padding: 0rem layout.$spacing-05;
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
