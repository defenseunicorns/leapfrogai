<script lang="ts">
  import { LFTextArea } from '$components';
  import { Button, Dropdown } from 'carbon-components-svelte';
  import { afterUpdate, onMount, tick } from 'svelte';
  import { threadsStore, toastStore } from '$stores';
  import { ArrowRight, Checkmark, StopFilledAlt, UserProfile } from 'carbon-icons-svelte';
  import { type Message as AIMessage, useAssistant, useChat } from 'ai/svelte';
  import { page } from '$app/stores';
  import { afterNavigate, beforeNavigate, goto } from '$app/navigation';
  import Message from '$components/Message.svelte';
  import { getMessageText } from '$helpers/threads';
  import { getUnixSeconds } from '$helpers/dates.js';
  import { NO_SELECTED_ASSISTANT_ID } from '$constants';

  import {
    delay,
    getMessages,
    isAssistantMessage,
    resetMessages,
    saveMessage,
    sortMessages,
    stopThenSave
  } from '$helpers/chatHelpers';
  import {
    ERROR_GETTING_AI_RESPONSE_TEXT,
    ERROR_GETTING_ASSISTANT_MSG_TEXT,
    ERROR_SAVING_MSG_TEXT
  } from '$constants/errorMessages';
  import type { PageServerLoad } from './$types';

  // TODO - this data is not receiving correct type inference, see issue: (https://github.com/defenseunicorns/leapfrogai/issues/587)
  export let data: PageServerLoad;

  /** LOCAL VARS **/
  let messageThreadDiv: HTMLDivElement;
  let messageThreadDivHeight: number;
  let lengthInvalid: boolean; // bound to child LFTextArea
  let assistantsList: Array<{ id: string; text: string }>;
  /** END LOCAL VARS **/

  /** REACTIVE STATE **/

  $: activeThread = $threadsStore.threads.find((t) => t.id === $page.params.thread_id);

  $: assistantsList = [...(data.assistants || [])].map((assistant) => ({
    id: assistant.id,
    text: assistant.name || 'unknown'
  }));
  $: assistantsList.unshift({ id: NO_SELECTED_ASSISTANT_ID, text: 'Select assistant...' }); // add dropdown item for no assistant selected
  $: assistantsList.push({ id: `manage-assistants`, text: 'Manage assistants' }); // add dropdown item for manage assistants button
  $: assistantMode =
    $threadsStore.selectedAssistantId !== NO_SELECTED_ASSISTANT_ID &&
    $threadsStore.selectedAssistantId !== 'manage-assistants';

  $: if ($isLoading || $status === 'in_progress') threadsStore.setSendingBlocked(true);

  // new streamed assistant message received (has no assistant_id)
  $: if (
    $assistantMessages.length > 0 &&
    !$assistantMessages[$assistantMessages.length - 1].assistant_id
  )
    modifyAndSaveAssistantMessage();

  $: sortedMessages = sortMessages([...$chatMessages, ...$assistantMessages]);

  /** END REACTIVE STATE **/

  const modifyAndSaveAssistantMessage = async () => {
    // Streamed assistant responses don't contain an assistant_id, so we add it here
    // and also add a createdAt date if not present
    const assistantMessagesCopy = [...$assistantMessages];
    const latestMessage = assistantMessagesCopy[assistantMessagesCopy.length - 1];

    latestMessage.assistant_id = $threadsStore.selectedAssistantId;
    if (!latestMessage.createdAt)
      latestMessage.createdAt = latestMessage.created_at || getUnixSeconds(new Date());

    setAssistantMessages(assistantMessagesCopy);
    // '/api/chat/assistants' saves the messages with the API to the db for us, so we re-fetch and update the store here
    await updateMessagesFromAPI();
    threadsStore.setSendingBlocked(false);
  };

  const updateMessagesFromAPI = async () => {
    const messages = await getMessages($page.params.thread_id);
    await threadsStore.updateMessages($page.params.thread_id, messages);
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
    onFinish: async (message: AIMessage) => {
      // OpenAI returns the creation timestamp in seconds instead of milliseconds.
      // If a response comes in quickly, we need to delay 1 second to ensure the timestamps of the user message
      // and AI response are not exactly the same. This is important for sorting messages when they are initially loaded
      // from the db/API (ex. browser refresh). Streamed messages are sorted realtime and we modify the timestamps to
      // ensure we have millisecond precision.
      threadsStore.setSendingBlocked(true);
      try {
        if (process.env.NODE_ENV !== 'test') await delay(1000);

        if (!assistantMode && activeThread?.id) {
          // Save with API to db
          const newMessage = await saveMessage({
            thread_id: activeThread.id,
            content: getMessageText(message),
            role: 'assistant'
          });

          await threadsStore.addMessageToStore(newMessage);
        }
        if (process.env.NODE_ENV !== 'test') await delay(1000); // ensure next user message has a different timestamp
      } catch {
        toastStore.addToast({
          kind: 'error',
          title: 'Error',
          subtitle: 'Error saving AI Response'
        });
      }
      threadsStore.setSendingBlocked(false);
    },
    onError: () => {
      toastStore.addToast({
        kind: 'error',
        title: ERROR_GETTING_AI_RESPONSE_TEXT.title,
        subtitle: ERROR_GETTING_AI_RESPONSE_TEXT.subtitle
      });
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
    threadId: activeThread?.id,
    onError: (e) => {
      // ignore this error b/c it is expected on cancel
      if (e.toString() !== 'DOMException: BodyStreamBuffer was aborted') {
        toastStore.addToast({
          kind: 'error',
          title: ERROR_GETTING_ASSISTANT_MSG_TEXT.title,
          subtitle: ERROR_GETTING_ASSISTANT_MSG_TEXT.subtitle
        });
      }
    }
  });

  const sendAssistantMessage = async (e: SubmitEvent | KeyboardEvent) => {
    if (activeThread?.id) {
      // assistant mode
      $assistantInput = $chatInput;
      $chatInput = ''; // clear chat input

      await submitAssistantMessage(e, {
        // submit to AI (/api/chat/assistants)
        data: {
          message: $chatInput,
          assistantId: $threadsStore.selectedAssistantId,
          threadId: activeThread.id
        }
      });
      $assistantInput = '';
    }
  };

  const sendChatMessage = async (e: SubmitEvent | KeyboardEvent) => {
    if (activeThread?.id) {
      // Save with API
      try {
        const newMessage = await saveMessage({
          thread_id: activeThread.id,
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
      }
    }
  };

  const onSubmit = async (e: SubmitEvent | KeyboardEvent) => {
    e.preventDefault();
    if ($threadsStore.sendingBlocked && activeThread?.id) {
      // message still sending
      await stopThenSave({
        activeThreadId: activeThread.id,
        messages: $chatMessages,
        status: $status,
        isLoading: $isLoading || false,
        assistantStop,
        chatStop
      });
      return;
    } else {
      if (!activeThread?.id) {
        // create new thread
        await threadsStore.newThread($chatInput);
        await tick(); // allow store to update
      }

      assistantMode ? await sendAssistantMessage(e) : await sendChatMessage(e);
    }
  };

  onMount(async () => {
    threadsStore.setThreads(data.threads || []);
    await tick();
    resetMessages({
      activeThread,
      setChatMessages,
      setAssistantMessages
    });
  });

  afterUpdate(() => {
    // Scroll to bottom
    messageThreadDiv.scrollTop = messageThreadDiv.scrollHeight;
  });

  beforeNavigate(async () => {
    if ($threadsStore.sendingBlocked && activeThread?.id) {
      await stopThenSave({
        activeThreadId: activeThread.id,
        messages: $chatMessages,
        status: $status,
        isLoading: $isLoading || false,
        assistantStop,
        chatStop
      });
    }
  });

  afterNavigate(() => {
    resetMessages({
      activeThread,
      setChatMessages,
      setAssistantMessages
    });
  });
</script>

<div class="chat-inner-content">
  <div class="messages" bind:this={messageThreadDiv} bind:offsetHeight={messageThreadDivHeight}>
    {#each sortedMessages as message, index (message.id)}
      <Message
        {message}
        messages={isAssistantMessage(message) ? $assistantMessages : $chatMessages}
        setMessages={isAssistantMessage(message) ? setAssistantMessages : setChatMessages}
        isLastMessage={index === sortedMessages.length - 1}
        append={isAssistantMessage(message) ? assistantAppend : chatAppend}
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
    outline: 1px solid themes.$border-subtle-03;
    :global(.bx--list-box__menu_item__option) {
      padding-right: 0.25rem;
    }
  }

  .noAssistant {
    :global(.bx--list-box__label) {
      color: themes.$text-secondary;
    }
  }
</style>
