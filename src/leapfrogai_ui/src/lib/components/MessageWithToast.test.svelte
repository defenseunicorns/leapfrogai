<script lang="ts">
  import { Message, Toasts } from '$components';
  import { type Message as AIMessage } from 'ai/svelte';
  import type { Message as OpenAIMessage } from 'openai/resources/beta/threads/messages';
  import type { AppendFunction, ReloadFunction } from '$lib/types/messages';

  export let message: AIMessage | OpenAIMessage;
  export let messages: AIMessage[] = [];
  export let setMessages: (messages: AIMessage[]) => void;
  export let isLastMessage: boolean;

  export let append: AppendFunction;
  export let reload: ReloadFunction;
</script>

<div>
  <Toasts />
  <Message {message} {messages} {setMessages} {isLastMessage} {append} {reload} />
</div>
