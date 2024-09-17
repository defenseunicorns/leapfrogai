<script lang="ts">
  import { beforeNavigate } from '$app/navigation';
  import { LFTextArea, PoweredByDU } from '$components';
  import { Hr, ToolbarButton } from 'flowbite-svelte';
  import { onMount, tick } from 'svelte';
  import { threadsStore, toastStore } from '$stores';
  import { type Message as VercelAIMessage, useAssistant, useChat } from '@ai-sdk/svelte';
  import { page } from '$app/stores';
  import Message from '$components/Message.svelte';
  import { getMessageText } from '$helpers/threads';
  import { getUnixSeconds } from '$helpers/dates.js';
  import { FILE_UPLOAD_PROMPT, NO_SELECTED_ASSISTANT_ID } from '$constants';
  import { twMerge } from 'tailwind-merge';
  import {
    isRunAssistantMessage,
    resetMessages,
    saveMessage,
    stopThenSave
  } from '$helpers/chatHelpers';
  import {
    ERROR_GETTING_AI_RESPONSE_TOAST,
    ERROR_GETTING_ASSISTANT_MSG_TOAST,
    ERROR_SAVING_MSG_TOAST
  } from '$constants/toastMessages';
  import SelectAssistantDropdown from '$components/SelectAssistantDropdown.svelte';
  import { PaperPlaneOutline, StopOutline } from 'flowbite-svelte-icons';
  import type { FileMetadata, LFFile } from '$lib/types/files';
  import UploadedFileCards from '$components/UploadedFileCards.svelte';
  import ChatFileUploadForm from '$components/ChatFileUpload.svelte';
  import FileChatActions from '$components/FileChatActions.svelte';

  export let data;

  /** LOCAL VARS **/
  let lengthInvalid: boolean; // bound to child LFTextArea
  let assistantsList: Array<{ id: string; text: string }>;
  let uploadingFiles = false;
  let attachedFiles: LFFile[] = []; // the actual files uploaded
  let attachedFileMetadata: FileMetadata[] = []; // metadata about the files uploaded, e.g. upload status, extracted text, etc...
  /** END LOCAL VARS **/

  /** REACTIVE STATE **/
  $: componentHasMounted = false;
  $: $page.params.thread_id, threadsStore.setLastVisitedThreadId($page.params.thread_id);
  $: $page.params.thread_id,
    resetMessages({
      activeThread: data.thread,
      setChatMessages,
      setAssistantMessages
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
  $: $chatMessages.length, updateStreamingChatMessage();

  // Handle streaming assistant messages
  $: $assistantMessages, handleAssistantMessage();

  // assistant stream has completed
  $: $status, handleCompletedAssistantResponse();

  $: sendDisabled = uploadingFiles || !$chatInput || lengthInvalid || $threadsStore.sendingBlocked;

  $: if (assistantMode) {
    resetFiles(); // attachment of files w/assistants disabled
  }

  /** END REACTIVE STATE **/

  const resetFiles = () => {
    uploadingFiles = false;
    attachedFileMetadata = [];
  };

  const updateStreamingChatMessage = () => {
    if ($isLoading && latestChatMessage?.role !== 'user')
      threadsStore.setStreamingMessage(latestChatMessage);
  };

  const handleAssistantMessage = async () => {
    if ($status === 'in_progress') {
      // The initial user message is stored with a short temp id by @ai-sdk/svelte, we need to wait for the
      // user message to be saved to the DB so we have the real id. Temp IDs appear to be 7 chars long, setting the
      // length check here higher for safety
      if (latestAssistantMessage?.role === 'user' && latestAssistantMessage.id.length > 15) {
        const userMessageId = $assistantMessages[$assistantMessages.length - 1].id;
        const messageRes = await fetch(
          `/api/messages?thread_id=${$page.params.thread_id}&message_id=${userMessageId}`
        );
        const message = await messageRes.json();
        // store the assistant id on the user msg to know it's associated with an assistant
        message.metadata.assistant_id = $threadsStore.selectedAssistantId;
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
    if (componentHasMounted && $status === 'awaiting_message') {
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
    append: chatAppend
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
        ...ERROR_GETTING_AI_RESPONSE_TOAST()
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
          ...ERROR_GETTING_ASSISTANT_MSG_TOAST()
        });
      }
      await threadsStore.setSendingBlocked(false);
    }
  });

  const sendAssistantMessage = async (e: SubmitEvent | KeyboardEvent) => {
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
    try {
      await threadsStore.setSendingBlocked(true);
      if (data.thread?.id) {
        let extractedFilesTextString = JSON.stringify(attachedFileMetadata);

        if (attachedFileMetadata.length > 0) {
          // Save the text of the document as its own message before sending actual question
          const contextMsg = await saveMessage({
            thread_id: data.thread.id,
            content: `${FILE_UPLOAD_PROMPT}: ${extractedFilesTextString}`,
            role: 'user',
            metadata: {
              hideMessage: 'true'
            },
            lengthOverride: true
          });
          threadsStore.updateMessagesState($chatMessages, setChatMessages, contextMsg);
        }

        // Save with API
        const newMessage = await saveMessage({
          thread_id: data.thread.id,
          content: $chatInput,
          role: 'user',
          ...(attachedFileMetadata.length > 0
            ? {
                metadata: {
                  filesMetadata: JSON.stringify(attachedFileMetadata)
                }
              }
            : null)
        });

        // store user input
        await threadsStore.addMessageToStore(newMessage);
        submitChatMessage(e); // submit to AI (/api/chat)
        resetFiles();
      }
    } catch {
      toastStore.addToast({
        ...ERROR_SAVING_MSG_TOAST()
      });
      await threadsStore.setSendingBlocked(false);
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
      if (sendDisabled) return;
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
    componentHasMounted = true;
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

<form on:submit={onSubmit} class="flex h-full flex-col">
  <div class="no-scrollbar flex flex-grow flex-col-reverse overflow-auto px-8">
    <div id="messages-container" data-testid="messages-container">
      {#each activeThreadMessages as message, index (message.id)}
        {#if message.metadata?.hideMessage !== 'true'}
          <Message
            messages={activeThreadMessages}
            streamedMessages={isRunAssistantMessage(message) ? $assistantMessages : $chatMessages}
            {message}
            isLastMessage={!$threadsStore.streamingMessage &&
              index === activeThreadMessages.length - 1}
            append={assistantMode ? assistantAppend : chatAppend}
            setMessages={isRunAssistantMessage(message) ? setAssistantMessages : setChatMessages}
          />
        {/if}
      {/each}

      {#if $threadsStore.streamingMessage}
        <Message message={$threadsStore.streamingMessage} isLastMessage />
      {/if}
    </div>
  </div>
  <Hr classHr="my-2" />
  <div id="chat-tools" data-testid="chat-tools" class="flex flex-col gap-2 px-8">
    <SelectAssistantDropdown assistants={data?.assistants || []} />

    <div
      class={twMerge(
        'flex flex-grow flex-col gap-2.5 rounded-lg bg-gray-50 px-4 py-0 dark:bg-gray-700',
        attachedFileMetadata.length > 0 && 'py-4'
      )}
    >
      <UploadedFileCards bind:attachedFileMetadata bind:attachedFiles />

      <div id="chat-row" class="flex w-full items-center gap-1">
        {#if !assistantMode}
          <ChatFileUploadForm bind:uploadingFiles bind:attachedFiles bind:attachedFileMetadata />
        {/if}
        <LFTextArea
          id="chat"
          data-testid="chat-input"
          class="flex-grow resize-none border-none bg-white focus:ring-0 dark:bg-gray-700"
          placeholder="Type your message here..."
          value={chatInput}
          bind:showLengthError={lengthInvalid}
          {onSubmit}
          maxRows={10}
          innerWrappedClass="p-px bg-white dark:bg-gray-700"
        />

        {#if !$isLoading && $status !== 'in_progress'}
          <ToolbarButton
            data-testid="send message"
            type="submit"
            color="blue"
            class={twMerge(
              'rounded-full text-primary-600 dark:text-primary-500',
              sendDisabled && 'hover:dark:bg-gray-700 '
            )}
            disabled={sendDisabled}
          >
            <PaperPlaneOutline
              class={twMerge('h-6 w-6 rotate-45', sendDisabled && 'text-primary-100')}
            />
            <span class="sr-only">Send message</span>
          </ToolbarButton>
        {:else}
          <ToolbarButton
            data-testid="cancel message"
            type="submit"
            color="gray"
            class="rounded-full text-primary-600 dark:text-primary-500"
            ><StopOutline class="h-6 w-6" color="red" /><span class="sr-only">Cancel message</span
            ></ToolbarButton
          >
        {/if}
      </div>
      <FileChatActions
        bind:attachedFileMetadata
        threadId={data.thread?.id}
        bind:attachedFiles
        originalMessages={$chatMessages}
        setMessages={setChatMessages}
      />
    </div>
  </div>
  <PoweredByDU />
</form>
