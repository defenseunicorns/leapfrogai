<!--
This component is a wrapper around a textarea that resizes the input until it reaches a limit of max rows, at which
point it begins to scroll.
The enter button calls onSubmit, but a user can still enter multiple lines of text with shift+enter.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import type { Writable } from 'svelte/store';

	export let value: Writable<string>;
	export let onSubmit: (e: SubmitEvent | KeyboardEvent) => Promise<void>;
	export let maxRows = 10;
	export let placeholder = 'Type your message here...';

	let inputHeight = '';
	let textAreaRef: HTMLTextAreaElement;

	function resizeTextArea() {
		textAreaRef.style.height = '1px';
		textAreaRef.style.height = textAreaRef.scrollHeight - 2 + 'px';
	}

	onMount(() => {
		const style = getComputedStyle(document.documentElement);
		inputHeight = style.getPropertyValue('--message-input-height').trim();
		resizeTextArea();
	});
</script>

<textarea
	bind:this={textAreaRef}
	bind:value={$value}
	on:input={resizeTextArea}
	on:keydown={(e) => {
		if (e.key === 'Enter' && !e.shiftKey) {
			textAreaRef.style.height = inputHeight; // reset input size if there were multiple lines
			onSubmit(e);
		}
	}}
	class="lf-text-area"
	class:bx--text-area={true}
	style="--maxRows:{maxRows};"
	name="messageInput"
	{placeholder}
	aria-label="message input"
	{...$$restProps}
/>

<style lang="scss">
	.lf-text-area,
	:global(.bx--text-area) {
		overflow-y: scroll;
		min-height: var(--message-input-height);
		max-height: calc(var(--maxRows) * 22px); // each row is 22px
		scrollbar-color: themes.$layer-03 themes.$layer-01;
		padding: 0.6rem 1rem; // need to slightly reduce padding to avoid having scroll bar initially
		resize: none;
	}
</style>
