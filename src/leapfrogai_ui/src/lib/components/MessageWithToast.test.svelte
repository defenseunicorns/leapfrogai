<script lang="ts">
  import { Message, Toasts } from '$components';
  import { type Message as AIMessage } from 'ai/svelte';

  export let message: AIMessage;
  export let handleMessageEdit: (
    event: SubmitEvent | KeyboardEvent | MouseEvent,
    message: AIMessage
  ) => Promise<void>;
  export let handleRegenerate: () => Promise<void>;
  export let isLastMessage: boolean;
  export let isLoading: boolean;
</script>

<div>
  <Toasts />
  <Message {message} {handleMessageEdit} {handleRegenerate} {isLastMessage} {isLoading} />
</div>
