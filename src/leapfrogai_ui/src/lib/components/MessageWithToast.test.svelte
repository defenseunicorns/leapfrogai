<script lang="ts">
  import { Message, Toasts } from '$components';
  import { type Message as AIMessage } from 'ai/svelte';
  import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';
  import type { ChatRequestOptions, CreateMessage } from 'ai';

  export let message: AIMessage | OpenAIMessage;
  export let messages: AIMessage[] = [];
  export let setMessages: (messages: AIMessage[]) => void;
  export let isLastMessage: boolean;
  export let isLoading: boolean;
  export let append: (
    message: AIMessage | CreateMessage,
    requestOptions?:
      | {
          data?: Record<string, string> | undefined;
        }
      | undefined
    // This any type matches the typing of the append function from Vercel AI
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  ) => Promise<any>;
  export let reload: (
    chatRequestOptions?: ChatRequestOptions | undefined
  ) => Promise<string | null | undefined>;
</script>

<div>
  <Toasts />
  <Message {message} {messages} {setMessages} {isLastMessage} {isLoading} {append} {reload} />
</div>
