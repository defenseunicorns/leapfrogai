<script lang="ts">
  import { LFTextArea } from '$components';
  import { Button, Dropdown } from 'carbon-components-svelte';
  import { afterUpdate, onMount, tick } from 'svelte';
  import { threadsStore, toastStore } from '$stores';
  import { ArrowRight, StopFilledAlt, UserProfile } from 'carbon-icons-svelte';
  import { type Message as AIMessage, useChat, useAssistant } from 'ai/svelte';
  import { page } from '$app/stores';
  import { beforeNavigate, goto } from '$app/navigation';
  import Message from '$components/Message.svelte';
  import type { LFMessage } from '$lib/types/messages';
  import { convertMessageToAiMessage, getMessageText } from '$helpers/threads';

  export let data;

  let messageThreadDiv: HTMLDivElement;
  let messageThreadDivHeight: number;
  let lengthInvalid: boolean; // bound to child LFTextArea

  let assistantsList: Array<{ id: string; text: string }>;
  let noSelectedAssistantId = `none-${new Date().toDateString()}`; // prevents id naming conflicts
  let selectedAssistantId: string = noSelectedAssistantId;
  $: assistantsList = [...data.assistants].map((assistant) => ({
    id: assistant.id,
    text: assistant.name || 'unknown'
  }));
  $: assistantMode =
    selectedAssistantId !== noSelectedAssistantId && selectedAssistantId !== 'manage-assistants';
  $: assistantsList.unshift({ id: noSelectedAssistantId, text: 'Select Assistant' }); // add dropdown item for no assistant selected
  $: assistantsList.push({ id: `manage-assistants`, text: 'Manage Assistants' }); // add dropdown item for manage assistants button

  $: activeThread = $threadsStore.threads.find((thread) => thread.id === $page.params.thread_id);
  $: $page.params.thread_id,
    setMessages(activeThread?.messages?.map((m) => convertMessageToAiMessage(m)) || []);

  const {
    input: chatInput,
    handleSubmit: submitChatMessage,
    messages,
    setMessages,
    isLoading,
    stop,
    append,
    reload,
  } = useChat({
    initialMessages: $threadsStore.threads
      .find((thread) => thread.id === $page.params.thread_id)
      ?.messages?.map((message: LFMessage) => ({
        id: message.id,
        content: getMessageText(message),
        role: message.role
      })),
    onFinish: async (message: AIMessage) => {
      if (activeThread?.id) {
        await threadsStore.newMessage({
          thread_id: activeThread?.id,
          content: message.content,
          role: message.role
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

  const {
    status,
    messages: assistantMessages,
    input: assistantInput,
    submitMessage: submitAssistantMessage
  } = useAssistant({
    api: '/api/chat/assistants',
    body: {
      threadId: activeThread?.id ? activeThread.id : null,
      message: $assistantInput,
      assistantId: selectedAssistantId
    }
  });

  const onSubmit = async (e: SubmitEvent | KeyboardEvent) => {
    e.preventDefault();

    if ($isLoading) {
      await stopThenSave();
    } else {
      if (!activeThread?.id) {
        // new thread thread
        await threadsStore.newThread($chatInput);
        await tick(); // allow store to update
        if (activeThread?.id) {
          await threadsStore.newMessage({
            thread_id: activeThread?.id,
            content: $chatInput,
            role: 'user'
          });
        }
      } else {
        // store user input
        await threadsStore.newMessage({
          thread_id: activeThread?.id,
          content: $chatInput,
          role: 'user'
        });
      }
      if (assistantMode) {
        $assistantInput = $chatInput;
        await submitAssistantMessage(e); // submit to AI (/api/chat/assistants)
      } else {
        submitChatMessage(e); // submit to AI (/api/chat)
      }
    }
  };

  const stopThenSave = async () => {
    if ($isLoading) {
      stop();
      toastStore.addToast({
        kind: 'info',
        title: 'Response Canceled',
        subtitle: 'Response generation canceled.'
      });
      const lastMessage = $messages[$messages.length - 1];

      if (activeThread?.id && lastMessage.role !== 'user') {
        await threadsStore.newMessage({
          thread_id: activeThread?.id,
          content: getMessageText(lastMessage), // save last message
          role: lastMessage.role
        });
      }
    }
  };

  const handleMessageEdit = async (
    event: SubmitEvent | KeyboardEvent | MouseEvent,
    message: AIMessage
  ) => {
    event.preventDefault();

    const messageIndex = $messages.findIndex((m) => m.id === message.id);
    // Ensure the message after the user's message exists and is a response from the AI
    const numToSplice =
      $messages[messageIndex + 1] && $messages[messageIndex + 1].role !== 'user' ? 2 : 1;

    if (activeThread?.id) {
      // delete old message from DB
      await threadsStore.deleteMessage(activeThread.id, message.id);
      if (numToSplice === 2) {
        // also delete that message's response
        await threadsStore.deleteMessage(activeThread.id, $messages[messageIndex + 1].id);
      }

      // save new message
      await threadsStore.newMessage({
        thread_id: activeThread.id,
        content: getMessageText(message),
        role: 'user'
      });
    }
    setMessages($messages.toSpliced(messageIndex, numToSplice)); // remove original message and response

    // send to /api/chat
    await append(message);
  };

  const handleRegenerate = async () => {
    const messageIndex = $messages.length - 1;
    if (activeThread?.id) {
      await threadsStore.deleteMessage(activeThread.id, $messages[messageIndex].id);
    }
    setMessages($messages.toSpliced(messageIndex, 1));
    await reload();
  };

  onMount(() => {
    threadsStore.setThreads(data.threads || []);
  });

  afterUpdate(() => {
    // Scroll to bottom
    messageThreadDiv.scrollTop = messageThreadDiv.scrollHeight;
  });

  beforeNavigate(async () => {
    if ($isLoading) {
      await stopThenSave();
    }
  });

  $: console.log([...$messages, ...$assistantMessages]);
</script>

<!--Note - the messages are streamed live from the useChat messages, saving them in the db and store happens behind the scenes -->
<div class="chat-inner-content">
  <div class="messages" bind:this={messageThreadDiv} bind:offsetHeight={messageThreadDivHeight}>
    {#each [...$messages, ...$assistantMessages] as message, index (message.id)}
      <Message
        {message}
        {handleMessageEdit}
        {handleRegenerate}
        isLastMessage={index === $messages.length - 1}
        isLoading={$isLoading || false}
      />
    {/each}
  </div>

  <hr id="divider" class="bx--switcher__item--divider divider" />
  <div class="chat-form-container">
    <form on:submit={onSubmit}>
      <Dropdown
        hideLabel
        direction="top"
        bind:selectedId={selectedAssistantId}
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

        {#if !$isLoading}
          <Button
            data-testid="send message"
            kind="secondary"
            icon={ArrowRight}
            size="field"
            type="submit"
            iconDescription="send"
            disabled={$isLoading || !$chatInput || lengthInvalid}
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
