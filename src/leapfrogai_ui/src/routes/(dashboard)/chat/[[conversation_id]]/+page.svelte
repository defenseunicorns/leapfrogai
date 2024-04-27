<script lang="ts">
	import { LFTextArea, PoweredByDU } from '$components';
	import { Button } from 'carbon-components-svelte';
	import { afterUpdate, onMount, tick } from 'svelte';
	import { conversationsStore, toastStore } from '$stores';
	import { ArrowRight, Attachment, StopFilledAlt } from 'carbon-icons-svelte';
	import { type Message as AIMessage, useChat } from 'ai/svelte';
	import { page } from '$app/stores';
	import { beforeNavigate } from '$app/navigation';
	import Message from '$components/Message.svelte';

	export let data;
	let messageThreadDiv: HTMLDivElement;
	let messageThreadDivHeight: number;

	$: activeConversation = $conversationsStore.conversations.find(
		(conversation) => conversation.id === $page.params.conversation_id
	);

	$: $page.params.conversation_id, setMessages(activeConversation?.messages || []);

	const { input, handleSubmit, messages, setMessages, isLoading, stop, append, reload } = useChat({
		initialMessages: $conversationsStore.conversations
			.find((conversation) => conversation.id === $page.params.conversation_id)
			?.messages.map((message) => ({
				id: message.id,
				content: message.content,
				role: message.role
			})),
		onFinish: async (message: AIMessage) => {
			if (activeConversation?.id) {
				await conversationsStore.newMessage({
					conversation_id: activeConversation?.id,
					content: message.content,
					role: message.role
				});
			}
		},
		onError: (error) => {
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
			if (!activeConversation?.id) {
				// new conversation thread
				await conversationsStore.newConversation($input);
				await tick(); // allow store to update
				if (activeConversation?.id) {
					await conversationsStore.newMessage({
						conversation_id: activeConversation?.id,
						content: $input,
						role: 'user'
					});
				}
			} else {
				// store user input
				await conversationsStore.newMessage({
					conversation_id: activeConversation?.id,
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

			if (activeConversation?.id && lastMessage.role !== 'user') {
				await conversationsStore.newMessage({
					conversation_id: activeConversation?.id,
					content: lastMessage.content, // save last message
					role: lastMessage.role
				});
			}
		}
	};

	const handleMessageEdit = async (e: any, message: AIMessage) => {
		e.preventDefault();

		const messageIndex = $messages.findIndex((m) => m.id === message.id);
		// Ensure the message after the user's message exists and is a response from the AI
		const numToSplice =
			$messages[messageIndex + 1] && $messages[messageIndex + 1].role !== 'user' ? 2 : 1;

		if (activeConversation?.id) {
			// delete old message from DB
			await conversationsStore.deleteMessage(message.id, activeConversation.id);
			if (numToSplice === 2) {
				// also delete that message's response
				await conversationsStore.deleteMessage(
					$messages[messageIndex + 1].id,
					activeConversation.id
				);
			}

			// save new message
			await conversationsStore.newMessage({
				conversation_id: activeConversation.id,
				content: message.content,
				role: 'user'
			});
		}
		setMessages($messages.toSpliced(messageIndex, numToSplice)); // remove original message and response

		// send to /api/chat
		await append(message);
	};

	const handleRegenerate = async () => {
		const messageIndex = $messages.length - 1;
		if (activeConversation?.id) {
			await conversationsStore.deleteMessage($messages[messageIndex].id, activeConversation.id);
		}
		setMessages($messages.toSpliced(messageIndex, 1))
		await reload();
	};

	onMount(() => {
		conversationsStore.setConversations(data.conversations);
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
<div class="inner-content">
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
			<Button icon={Attachment} kind="ghost" size="small" iconDescription="Attach File" />
			<LFTextArea value={input} {onSubmit} />

			{#if !$isLoading}
				<Button
					data-testid="send message"
					kind="secondary"
					icon={ArrowRight}
					size="field"
					type="submit"
					iconDescription="send"
					disabled={$isLoading || !$input}
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

	<div class="branding">
		<PoweredByDU />
	</div>
</div>

<style lang="scss">
	.inner-content {
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

	.branding {
		margin: layout.$spacing-05 0 layout.$spacing-05 0;
	}
</style>
