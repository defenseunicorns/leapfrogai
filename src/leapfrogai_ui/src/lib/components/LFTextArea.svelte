<script lang="ts">
	import { onMount } from 'svelte';
	import type { Writable } from 'svelte/store';

	export let value: Writable<string>;
	export let onSubmit: (e: SubmitEvent | KeyboardEvent) => Promise<void>;

	let textAreaRef: HTMLTextAreaElement;

	function resizeTextArea() {
		textAreaRef.style.height = '1px';
		textAreaRef.style.height = textAreaRef.scrollHeight - 2 + 'px';
	}

	onMount(() => {
		resizeTextArea();
	});
</script>

<textarea
	bind:this={textAreaRef}
	bind:value={$value}
	on:input={resizeTextArea}
	on:keydown={(e) => {
		if (e.key === 'Enter' && !e.shiftKey) {
			textAreaRef.style.height = '2.7rem'; // reset input size if there were multiple lines
			onSubmit(e);
		}
	}}
	class="lf-text-area"
	class:bx--text-area={true}
	name="messageInput"
	placeholder="Type your message here..."
	aria-label="message input"
	{...$$restProps}
/>

<style lang="scss">
	.lf-text-area,
	:global(.bx--text-area) {
		overflow-y: scroll;
		height: 2.5rem;
		min-height: 2.7rem; // default is 2.5, but this prevents scrollbar from appearing when empty
		max-height: 220px; // equal to 10 rows
		scrollbar-color: themes.$layer-03 themes.$layer-01;
		resize: none;
	}
</style>
