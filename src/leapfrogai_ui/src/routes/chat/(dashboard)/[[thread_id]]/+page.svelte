<script lang="ts">
  import { LFTextArea } from '$components';
  import { Button } from 'carbon-components-svelte';
  import { afterUpdate, onMount, tick } from 'svelte';
  import { threadsStore, toastStore } from '$stores';
  import { ArrowRight, StopFilledAlt } from 'carbon-icons-svelte';
  import { type Message as AIMessage, useChat } from 'ai/svelte';
  import { page } from '$app/stores';
  import { beforeNavigate } from '$app/navigation';
  import Message from '$components/Message.svelte';
  import type { LFMessage } from '$lib/types/messages';
  import { convertMessageToAiMessage, getMessageText } from '$helpers/threads';

  export let data;

  let messageThreadDiv: HTMLDivElement;
  let messageThreadDivHeight: number;

  let lengthInvalid: boolean; // bound to child LFTextArea

  $: activeThread = $threadsStore.threads.find((thread) => thread.id === $page.params.thread_id);

  $: $page.params.thread_id,
    setMessages(activeThread?.messages?.map((m) => convertMessageToAiMessage(m)) || []);

  const { input, handleSubmit, messages, setMessages, isLoading, stop, append, reload } = useChat({
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

  const onSubmit = async (e: SubmitEvent | KeyboardEvent) => {
    e.preventDefault();

    if ($isLoading) {
      await stopThenSave();
    } else {
      if (!activeThread?.id) {
        // new thread thread
        await threadsStore.newThread($input);
        await tick(); // allow store to update
        if (activeThread?.id) {
          await threadsStore.newMessage({
            thread_id: activeThread?.id,
            content: $input,
            role: 'user'
          });
        }
      } else {
        // store user input
        await threadsStore.newMessage({
          thread_id: activeThread?.id,
          content: $input,
          role: 'user'
        });
      }

      handleSubmit(e); // submit to AI (/api/chat)
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
</script>

<!--Note - the messages are streamed live from the useChat messages, saving them in the db and store happens behind the scenes -->
<div class="chat-inner-content">
  <div class="messages" bind:this={messageThreadDiv} bind:offsetHeight={messageThreadDivHeight}>
    {#each $messages as message, index (message.id)}
      <Message
        {message}
        {handleMessageEdit}
        {handleRegenerate}
        isLastMessage={index === $messages.length - 1}
        isLoading={$isLoading || false}
      />
    {/each}
  </div>

  <form on:submit={onSubmit}>
    <div class="chat-form-container">
      <LFTextArea
        value={input}
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
          disabled={$isLoading || !$input || lengthInvalid}
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
  }

  .chat-form-container {
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    gap: 0.5rem;
  }
</style>
