<script lang="ts">
  import { LFTextArea } from '$components';
  import { Button, Dropdown } from 'carbon-components-svelte';
  import { afterUpdate, onMount, tick } from 'svelte';
  import { threadsStore, toastStore } from '$stores';
  import { ArrowRight, StopFilledAlt, UserProfile } from 'carbon-icons-svelte';
  import { type Message as AIMessage, useAssistant, useChat } from 'ai/svelte';
  import { page } from '$app/stores';
  import { beforeNavigate, goto, invalidate } from '$app/navigation';
  import Message from '$components/Message.svelte';
  import type { LFMessage } from '$lib/types/messages';
  import { convertMessageToAiMessage, getMessageText } from '$helpers/threads';
  import { getUnixSeconds } from '$helpers/dates.js';
  import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';

  export let data;

  $: activeThread = data.thread;
  $: originalMessages = data.messages;

  // TODO - check mark for selected assistant

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

  // Used to reset messages when thread id changes
  const resetMessages = () => {
    if (originalMessages && originalMessages.length > 0) {
      setMessages(
        originalMessages
          .map((m) => convertMessageToAiMessage(m))
          .sort((a, b) => a.created_at - b.created_at)
      );
      assistantSetMessages([]);
    } else {
      setMessages([]);
      assistantSetMessages([]);
    }
  };

  $: $page.params.thread_id, resetMessages();

  const getAssistantImage = (assistant_id: string) => {
    const myAssistant = data.assistants.find((assistant) => assistant.id === assistant_id);
    if (myAssistant) return myAssistant.metadata.avatar ?? myAssistant.metadata.pictogram;
    return null;
  };

  const {
    input: chatInput,
    handleSubmit: submitChatMessage,
    messages,
    setMessages,
    isLoading,
    stop,
    append,
    reload
  } = useChat({
    onFinish: async (message: AIMessage) => {
      if (!assistantMode && activeThread?.id) {
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
    input: assistantInput,
    messages: assistantMessages,
    submitMessage: submitAssistantMessage,
    stop: assistantStop,
    setMessages: assistantSetMessages,
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
    updatedMessages[messageIndex].assistant_id = selectedAssistantId;

    assistantSetMessages(updatedMessages);
  }

  $: messageInProgress = $isLoading || $status === 'in_progress';

  const onSubmit = async (e: SubmitEvent | KeyboardEvent) => {
    e.preventDefault();

    if (messageInProgress) {
      await stopThenSave();
    } else {
      if (!activeThread?.id) {
        // new thread
        await threadsStore.newThread($chatInput);
        await tick(); // allow store to update

        // If in chat mode, save the messages with store methods
        // Assistant API saves the messages itself
        if (!assistantMode && activeThread?.id) {
          await threadsStore.newMessage({
            thread_id: activeThread?.id,
            content: $chatInput,
            role: 'user'
          });
        }
      } else {
        if (!assistantMode) {
          // store user input
          await threadsStore.newMessage({
            thread_id: activeThread?.id,
            content: $chatInput,
            role: 'user'
          });
        }
      }

      if (assistantMode) {
        $assistantInput = $chatInput;
        $chatInput = '';

        await submitAssistantMessage(e, {
          // submit to AI (/api/chat/assistants)
          data: {
            message: $chatInput,
            assistantId: selectedAssistantId,
            threadId: activeThread?.id || ''
          }
        });
        $assistantInput = '';
      } else {
        submitChatMessage(e); // submit to AI (/api/chat)
      }
    }
  };

  const stopThenSave = async () => {
    // Note - assistantStop does not cancel the actual run, it only stops the stream
    // If you try to send another message while the run is still running on the server,
    // you will get an error.
    // issue opened for this here: https://github.com/vercel/ai/issues/1743
    if ($status === 'in_progress') assistantStop();
    else {
      if ($isLoading) {
        stop();
        const lastMessage = $messages[$messages.length - 1];

        if (activeThread?.id && lastMessage.role !== 'user') {
          await threadsStore.newMessage({
            thread_id: activeThread?.id,
            content: getMessageText(lastMessage), // save last message
            role: lastMessage.role
          });
        }
      }
    }

    toastStore.addToast({
      kind: 'info',
      title: 'Response Canceled',
      subtitle: 'Response generation canceled.'
    });
  };

  // TODO - create reg message, create assistant message, create regular message, order gets messed up
  // TODO - there's a sequence of events that that removes the assistant from an edited message
  const handleMessageEdit = async (
    event: SubmitEvent | KeyboardEvent | MouseEvent,
    message: AIMessage
  ) => {
    event.preventDefault();

    if (message.assistant_id && message.assistant_id !== noSelectedAssistantId) {
      selectedAssistantId = message.assistant_id; // set the assistant in the dropdown
      const messageIndex = $assistantMessages.findIndex((m) => m.id === message.id);
      // Ensure the message after the user's message exists and is a response from the AI
      const numToSplice =
        $assistantMessages[messageIndex + 1] && $assistantMessages[messageIndex + 1].role !== 'user'
          ? 2
          : 1;

      const deleteRes1 = await fetch('/api/messages/delete', {
        method: 'DELETE',
        body: JSON.stringify({ thread_id: activeThread?.id, message_id: message.id }),
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!deleteRes1.ok) {
        toastStore.addToast({
          kind: 'error',
          title: 'Error Editing Message',
          subtitle: 'Editing cancelled'
        });
        return;
      }

      if (numToSplice === 2) {
        const deleteRes2 = await fetch('/api/messages/delete', {
          method: 'DELETE',
          body: JSON.stringify({
            thread_id: activeThread?.id,
            message_id: $assistantMessages[messageIndex + 1].id
          }),
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (!deleteRes2.ok) {
          toastStore.addToast({
            kind: 'error',
            title: 'Error Editing Message',
            subtitle: 'Editing Cancelled'
          });
          return;
        }
      }
      assistantSetMessages($assistantMessages.toSpliced(messageIndex, numToSplice));
      // send to /api/chat/assistants
      await assistantAppend(
        { ...message, createdAt: undefined },
        {
          data: {
            message: message.content,
            assistantId: selectedAssistantId,
            threadId: activeThread?.id || ''
          }
        }
      );
    } else {
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
      await append({ ...message, createdAt: undefined });
    }
  };

  const handleRegenerate = async () => {
    const lastMessageIndex = filteredMessages.length - 1;
    const userMessage = filteredMessages[lastMessageIndex - 1];
    const response = filteredMessages[lastMessageIndex];

    if (response.assistant_id && response.assistant_id !== noSelectedAssistantId) {
      // is assistant response
      // useAssistant doesn't have a reload function, so we delete both the user message and the assistant response,
      // then manually append
      selectedAssistantId = response.assistant_id; // set the assistant in the dropdown
      const deleteRes1 = await fetch('/api/messages/delete', {
        method: 'DELETE',
        body: JSON.stringify({ thread_id: activeThread?.id, message_id: response.id }),
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!deleteRes1.ok) {
        toastStore.addToast({
          kind: 'error',
          title: 'Error Regenerating Message',
          subtitle: 'Regeneration cancelled'
        });
        return;
      }
      const deleteRes2 = await fetch('/api/messages/delete', {
        method: 'DELETE',
        body: JSON.stringify({ thread_id: activeThread?.id, message_id: userMessage.id }),
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!deleteRes2.ok) {
        toastStore.addToast({
          kind: 'error',
          title: 'Error Regenerating Message',
          subtitle: 'Regeneration cancelled'
        });
        return;
      }
      assistantSetMessages($assistantMessages.toSpliced(-2, 2));

      await assistantAppend(
        { ...userMessage, createdAt: undefined },
        {
          data: {
            message: userMessage.content,
            assistantId: selectedAssistantId,
            threadId: activeThread?.id || ''
          }
        }
      );
    } else if (activeThread?.id) {
      // TODO - can we use the threadsStore.deleteMessage method for the assistants too
      await threadsStore.deleteMessage(activeThread.id, response.id);
      setMessages($messages.toSpliced(-2, 2));

      await reload();
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
    if (messageInProgress) {
      await stopThenSave();
    }
  });

  $: filteredMessages = [...$assistantMessages, ...$messages].sort((a, b) => {
    if (!a.createdAt) a.createdAt = new Date();
    if (!b.createdAt) b.createdAt = new Date();

    return getUnixSeconds(a.createdAt) - getUnixSeconds(b.createdAt);
  });
</script>

<!--Note - the messages are streamed live from the useChat messages, saving them in the db and store happens behind the scenes -->
<div class="chat-inner-content">
  <div class="messages" bind:this={messageThreadDiv} bind:offsetHeight={messageThreadDivHeight}>
    {#each filteredMessages as message, index (message.id)}
      <Message
        {message}
        {handleMessageEdit}
        {handleRegenerate}
        isLastMessage={index === filteredMessages.length - 1}
        isLoading={messageInProgress || false}
        assistantImage={message.assistant_id ? getAssistantImage(message.assistant_id) : null}
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
