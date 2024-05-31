<script lang="ts">
  import { LFTextArea } from '$components';
  import { Button, Dropdown } from 'carbon-components-svelte';
  import { afterUpdate, onMount, tick } from 'svelte';
  import { threadsStore, toastStore } from '$stores';
  import { ArrowRight, StopFilledAlt, UserProfile } from 'carbon-icons-svelte';
  import { type Message as AIMessage, useAssistant, useChat } from 'ai/svelte';
  import { page } from '$app/stores';
  import { beforeNavigate, goto } from '$app/navigation';
  import Message from '$components/Message.svelte';
  import { convertMessageToAiMessage, getMessageText } from '$helpers/threads';
  import { getUnixSeconds } from '$helpers/dates.js';
  import { NO_SELECTED_ASSISTANT_ID } from '$constants';
  import { createMessage, isAssistantMessage, stopThenSave } from '$helpers/chatHelpers';

  export let data;

  // TODO - check mark for selected assistant

  /** LOCAL VARS **/
  let messageThreadDiv: HTMLDivElement;
  let messageThreadDivHeight: number;
  let lengthInvalid: boolean; // bound to child LFTextArea
  let assistantsList: Array<{ id: string; text: string }>;

  /** END LOCAL VARS **/

  /** REACTIVE STATE **/

  $: activeThread = data.thread;
  $: originalMessages = data.messages;

  $: assistantsList = [...data.assistants].map((assistant) => ({
    id: assistant.id,
    text: assistant.name || 'unknown'
  }));
  $: assistantsList.unshift({ id: NO_SELECTED_ASSISTANT_ID, text: 'Select Assistant' }); // add dropdown item for no assistant selected
  $: assistantsList.push({ id: `manage-assistants`, text: 'Manage Assistants' }); // add dropdown item for manage assistants button

  $: assistantMode =
    $threadsStore.selectedAssistantId !== NO_SELECTED_ASSISTANT_ID &&
    $threadsStore.selectedAssistantId !== 'manage-assistants';

  $: $page.params.thread_id, resetMessages();
  $: messageInProgress = $isLoading || $status === 'in_progress';

  // Assistant messages streamed to the client do not have an assistant_id field. We need to add it so the
  // assistant avatars and pictograms display.
  // Messages from assistants will get the last active assistant used.
  // When the page is refreshed, the messages are retrieved from the API and have the correct assistant_id assigned to them
  $: if (
    $assistantMessages.length > 0 &&
    !$assistantMessages[$assistantMessages.length - 1].assistant_id
  ) {
    const updatedMessages = [...$assistantMessages];
    const messageIndex = updatedMessages.findIndex(
      (m) => m.id === $assistantMessages[$assistantMessages.length - 1].id
    );
    updatedMessages[messageIndex].assistant_id = $threadsStore.selectedAssistantId;

    setAssistantMessages(updatedMessages);
  }
  $: combinedMessages = [...$assistantMessages, ...$chatMessages].sort((a, b) => {
    if (a.created_at && b.created_at) {
      if (a.createdAt === b.createdAt) {
        if (a.role === 'user' && b.role === 'assistant') {
          return -1; // 'user' should come first
        } else if (a.role === 'assistant' && b.role === 'user') {
          return 1; // 'assistant' should come after
        }
        return 0; // No change in order if roles are the same
      }
      return a.created_at - b.created_at;
    }
    if (!a.createdAt) a.createdAt = new Date();
    if (!b.createdAt) b.createdAt = new Date();

    return getUnixSeconds(a.createdAt) - getUnixSeconds(b.createdAt);
  });
  /** END REACTIVE STATE **/

  // Used to reset messages when thread id changes
  const resetMessages = () => {
    if (originalMessages && originalMessages.length > 0) {
      const assistantMessages = originalMessages
        .filter((m) => m.run_id)
        .map(convertMessageToAiMessage);
      const chatMessages = originalMessages.filter((m) => !m.run_id).map(convertMessageToAiMessage);

      setAssistantMessages(assistantMessages);
      setChatMessages(chatMessages);
    } else {
      setChatMessages([]);
      setAssistantMessages([]);
    }
  };

  /** useChat **/
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
    onFinish: async (message: AIMessage) => {
      try {
        if (!assistantMode && activeThread?.id) {
          // Save with API
          const newMessage = await createMessage({
            thread_id: activeThread.id,
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
    },
    onError: () => {
      toastStore.addToast({
        kind: 'error',
        title: 'Error',
        subtitle: 'Error getting AI Response'
      });
    }
  });

  /** useAssistant **/
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
      if (e.toString() !== 'DOMException: BodyStreamBuffer was aborted') {
        // this error is expected on cancel
        toastStore.addToast({
          kind: 'error',
          title: 'Error',
          subtitle: 'Error getting Assistant Response'
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
      const newMessage = await createMessage({
        thread_id: activeThread.id,
        content: $chatInput,
        role: 'user'
      });

      // store user input
      await threadsStore.addMessageToStore(newMessage);
      console.log($chatMessages);
      submitChatMessage(e); // submit to AI (/api/chat)
    }
  };

  const onSubmit = async (e: SubmitEvent | KeyboardEvent) => {
    e.preventDefault();

    if (messageInProgress && activeThread?.id) {
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

        // If in chat mode, save the messages with store methods
        // Assistant API saves the messages itself
        if (assistantMode) {
          await sendAssistantMessage(e);
        } else {
          await sendChatMessage(e);
        }
      } else {
        // active thread exists
        if (assistantMode) {
          await sendAssistantMessage(e);
        } else {
          await sendChatMessage(e);
        }
      }
    }
  };

  onMount(() => {
    threadsStore.setThreads(data.threads || []);
  });

  afterUpdate(() => {
    // Scroll to bottom
    messageThreadDiv.scrollTop = messageThreadDiv.scrollHeight;
  });

  beforeNavigate(async () => {
    if (messageInProgress && activeThread?.id) {
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
</script>

<div class="chat-inner-content">
  <div class="messages" bind:this={messageThreadDiv} bind:offsetHeight={messageThreadDivHeight}>
    {#each combinedMessages as message, index (message.id)}
      <Message
        {message}
        messages={isAssistantMessage(message) ? $assistantMessages : $chatMessages}
        setMessages={isAssistantMessage(message) ? setAssistantMessages : setChatMessages}
        isLastMessage={index === combinedMessages.length - 1}
        isLoading={messageInProgress || false}
        append={isAssistantMessage(message) ? assistantAppend : chatAppend}
        {reload}
      />
    {/each}
  </div>

  <hr id="divider" class="bx--switcher__item--divider divider" />
  <div class="chat-form-container">
    <form on:submit={onSubmit}>
      <Dropdown
        disabled={messageInProgress}
        hideLabel
        direction="top"
        selectedId={$threadsStore.selectedAssistantId}
        on:select={(e) => threadsStore.setSelectedAssistantId(e.detail.selectedId)}
        items={assistantsList}
        style="width: 25%; margin-bottom: 0.5rem"
        let:item
      >
        {#if item.id === `manage-assistants`}
          <div class="manage-assistants-btn" on:click={() => goto('/chat/assistants-management')}>
            <UserProfile />
            {item.text}
          </div>
        {:else}
          <div>
            {item.text}
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
            disabled={!$chatInput || lengthInvalid}
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

  .divider {
    width: 100%;
    margin: 0.5rem 0;
  }

  .manage-assistants-btn {
    display: flex;
    align-items: center;
    gap: layout.$spacing-03;
  }

  :global(#manage-assistants) {
    outline: 1px solid themes.$border-subtle-03;
  }
</style>
