<script lang="ts">
	import { ChatSidebar, PoweredByDU } from '$components';
	import { Button, Content, TextInput, Tile } from 'carbon-components-svelte';
	import { afterUpdate, onMount, tick } from 'svelte';
	import { conversationsStore, toastStore } from '$stores';
	import { ArrowRight, Attachment, UserAvatar } from 'carbon-icons-svelte';
	import { type Message as AIMessage, useChat } from 'ai/svelte';
	import frog from '$assets/frog.png';
	import { page } from '$app/stores';
	import { beforeNavigate } from '$app/navigation';

	export let data;
	let messageThreadDiv: HTMLDivElement;
	let messageThreadDivHeight: number;

	$: activeConversation = $conversationsStore.conversations.find(
		(conversation) => conversation.id === $page.params.conversation_id
	);

	$: $page.params.conversation_id, setMessages(activeConversation?.messages || []);

	const { input, handleSubmit, messages, setMessages, isLoading, stop, error } = useChat({
		initialMessages: $conversationsStore.conversations
			.find((conversation) => conversation.id === $page.params.conversation_id)
			?.messages.map((message) => ({
				id: message.id,
				content: message.content,
				role: message.role
			})),
		onFinish: async (message: AIMessage) => {
			if (activeConversation?.id) {
				await conversationsStore.newMessage(activeConversation?.id, message.content, 'system');
			}
		}
	});

	$: if ($error)
		toastStore.addToast({
			kind: 'error',
			title: 'Error',
			subtitle: 'Error getting AI Response'
		});

	const onSubmit = async (e: SubmitEvent) => {
		e.preventDefault();
		if (!activeConversation?.id) {
			// new conversation thread
			await conversationsStore.newConversation($input);
			await tick(); // allow store to update
			if (activeConversation?.id) {
				await conversationsStore.newMessage(activeConversation?.id, $input, 'user');
			}
		} else {
			// store user input
			await conversationsStore.newMessage(activeConversation?.id, $input, 'user');
		}

		handleSubmit(e); // submit to AI (/api/chat)
	};

	const stopThenSave = async () => {
		if ($isLoading) {
			stop();
			if (activeConversation?.id) {
				await conversationsStore.newMessage(
					activeConversation?.id,
					$messages[$messages.length - 1].content, // save last message
					'system'
				);
			}
		}
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
<div>
	<ChatSidebar />
	<Content>
		<div class="inner-content">
			<div class="messages" bind:this={messageThreadDiv} bind:offsetHeight={messageThreadDivHeight}>
				{#each $messages as message (message.id)}
					<div
						data-testid="message"
						class="message"
						class:transparent={message.role === 'user'}
						class:centered-vertically={message.role === 'user'}
					>
						{#if message.role === 'user'}
							<div class="icon">
								<UserAvatar style="width: 24px; height: 24px;" />
							</div>
						{:else}
							<img alt="LeapfrogAI" src={frog} class="icon" />
						{/if}
						<Tile class="centered-vertically" style="line-height: 20px;">{message.content}</Tile>
					</div>
				{/each}
			</div>

			<form on:submit={onSubmit}>
				<div class="chat-form-container">
					<Button icon={Attachment} kind="ghost" size="small" iconDescription="Attach File" />
					<TextInput
						bind:value={$input}
						name="messageInput"
						placeholder="Type your message here..."
						aria-label="message input"
					/>

					<Button
						kind="secondary"
						icon={ArrowRight}
						iconDescription="Send"
						size="field"
						type="submit"
						aria-label="send"
						disabled={$isLoading || !$input}
					/>
				</div>
			</form>

			<div class="branding">
				<PoweredByDU />
			</div>
		</div>
	</Content>
</div>

<style lang="scss">
	.centered-vertically,
	:global(.centered-vertically.bx--tile) {
		display: flex;
		align-items: center;
	}

	.message {
		display: flex;
	}

	.transparent {
		:global(.bx--tile) {
			background-color: transparent;
		}
	}

	.icon {
		width: 32px;
		height: 52px;
		padding: 14px layout.$spacing-02;
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
		align-items: center;
		gap: 0.5rem;
	}

	.inner-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
	}

	:global(.bx--content) {
		display: flex;
		flex: 1;
		margin-top: var(--header-height);
		padding-bottom: 0;
		// A few pixels are being added somewhere, so -0.5rem required to prevent scrollbar, not sure where it is coming from
		height: calc(100vh - var(--header-height) - 0.5rem);
	}

	.branding {
		margin: layout.$spacing-05 0 layout.$spacing-05 0;
	}
</style>
