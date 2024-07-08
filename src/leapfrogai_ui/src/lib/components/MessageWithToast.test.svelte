<script lang="ts">
  import { Message, Toasts } from '$components';
  import { type Message as VercelAIMessage } from 'ai/svelte';

  import type { AppendFunction, ReloadFunction, VercelOrOpenAIMessage } from '$lib/types/messages';

  export let allStreamedMessages: VercelAIMessage[];
  export let message: VercelOrOpenAIMessage;
  export let messages: VercelAIMessage[] = [];
  export let setMessages: (messages: VercelAIMessage[]) => void;
  export let isLastMessage: boolean;

  export let append: AppendFunction;
  export let reload: ReloadFunction;
</script>

<div>
  <Toasts />
  <Message
    {allStreamedMessages}
    {message}
    {messages}
    {setMessages}
    {isLastMessage}
    {append}
    {reload}
  />
</div>
