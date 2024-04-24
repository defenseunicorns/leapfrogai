<script lang="ts">
	import { Button, Tile } from 'carbon-components-svelte';
	import { Edit, UserAvatar } from 'carbon-icons-svelte';
	import { type Message as AIMessage } from 'ai/svelte';
	import { LFTextArea } from '$components';
	import frog from '$assets/frog.png';
	import { writable } from 'svelte/store';

	export let handleMessageEdit: (event: any, message: AIMessage) => Promise<void>;
	export let message: AIMessage;
	let messageIsHovered = false;
	let editMode = false;
	let value = writable(message.content);

	const onSubmit = async (e: SubmitEvent | KeyboardEvent | MouseEvent) => {
		editMode = false;
		await handleMessageEdit(e, { ...message, content: $value });
	};

	const handleCancel = () => {
		editMode = false;
		value.set(message.content); // restore original value
	};
</script>

<div
	data-testid="message"
	class="message"
	class:transparent={message.role === 'user'}
	on:mouseover={() => (messageIsHovered = true)}
	on:mouseleave={() => (messageIsHovered = false)}
>
	<div class="message-and-avatar">
		{#if message.role === 'user'}
			<div class="icon">
				<UserAvatar style="width: 24px; height: 24px;" />
			</div>
		{:else}
			<img alt="LeapfrogAI" src={frog} class="icon" />
		{/if}

		<div style="width: 100%">
			{#if editMode}
				<div class="edit-prompt">
					<LFTextArea {value} {onSubmit} />
					<div class="cancel-save">
						<Button size="small" kind="secondary" on:click={handleCancel}>Cancel</Button>
						<Button size="small" on:click={onSubmit}>Submit</Button>
					</div>
				</div>
			{:else}
				<Tile style="line-height: 20px;">{message.content}</Tile>
			{/if}

			{#if message.role === 'user' && !editMode}
				<div class="edit-prompt-icon" class:hide={!messageIsHovered}>
					<span on:click={() => (editMode = true)}><Edit aria-label="edit prompt" /></span>
				</div>
			{/if}
		</div>
	</div>
</div>

<style lang="scss">
	.message-and-avatar {
		display: flex;
		flex: 1;
		align-items: flex-start;
	}

	.hide {
		opacity: 0;
		transition: opacity 0.2s;
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

	.cancel-save {
		display: flex;
		justify-content: flex-end;
		gap: layout.$spacing-02;
	}

	.edit-prompt-icon :global(svg) {
		cursor: pointer;
		fill: themes.$icon-secondary;
		&:hover {
			fill: themes.$icon-primary;
		}
	}

	.edit-prompt :global(.lf-text-area.bx--text-area) {
		background: themes.$background;
		border: 1px solid themes.$layer-02;
	}
</style>
