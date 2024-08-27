<script lang="ts">
  import { Message, Toasts } from '$components';
  import { type Message as VercelAIMessage } from '@ai-sdk/svelte';

  import type { AppendFunction } from '$lib/types/messages';
  import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';

  export let message: OpenAIMessage;
  export let messages: OpenAIMessage[] = [];
  export let streamedMessages: VercelAIMessage[] = [];
  export let setMessages: ((messages: VercelAIMessage[]) => void) | undefined = undefined;
  export let isLastMessage: boolean;
  export let append: AppendFunction | undefined = undefined;
</script>

<div>
  <Toasts />
  <Message {message} {messages} {streamedMessages} {setMessages} {isLastMessage} {append} />
</div>
