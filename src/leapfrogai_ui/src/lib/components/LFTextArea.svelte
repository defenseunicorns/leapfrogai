<!--
This component is a wrapper around a textarea that resizes the input until it reaches a limit of max rows, at which
point it begins to scroll.
The enter button calls onSubmit, but a user can still enter multiple lines of text with shift+enter.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import type { Writable } from 'svelte/store';
	import { env } from '$env/dynamic/public';
	import { WarningFilled } from 'carbon-icons-svelte';
	export let value: Writable<string>;
	export let onSubmit: (e: SubmitEvent | KeyboardEvent) => Promise<void>;
	export let maxRows = 10;
	export let placeholder = 'Type your message here...';
	export let ariaLabel = 'message input';

	export let invalid = false;
	export let invalidText = '';
	export let helperText = "";
	export let disabled = false;
	export let id = 'ccs-' + Math.random().toString(36);


	let inputHeight = '';
	let textAreaRef: HTMLTextAreaElement;

	$: errorId = `error-${id}`;

	function resizeTextArea() {
		if ($value.length === Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT)) {
			console.log('too long');
		}
		textAreaRef.style.height = '1px';
		textAreaRef.style.height = textAreaRef.scrollHeight - 2 + 'px';
	}

	onMount(() => {
		const style = getComputedStyle(document.documentElement);
		inputHeight = style.getPropertyValue('--message-input-height').trim();
		resizeTextArea();
	});
</script>

{#if invalid}
	<WarningFilled class="bx--text-area__invalid-icon" />
{/if}
<textarea
	aria-invalid={invalid || undefined}
	aria-describedby={invalid ? errorId : undefined}
	disabled="{disabled}"
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
	class:error={invalid}
	style="--maxRows:{maxRows};"
	name="messageInput"
	{placeholder}
	maxlength={Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT) + 1}
	aria-label={ariaLabel}
	{...$$restProps}
/>

{#if !invalid && helperText}
	<div
			class:bx--form__helper-text="{true}"
			class:bx--form__helper-text--disabled="{disabled}"
	>
		{helperText}
	</div>
{/if}

{#if invalid}
	<div id="{errorId}" class:bx--form-requirement="{true}">{invalidText}</div>
{/if}

<style lang="scss">
	.error {
		border: 1px solid red;
	}

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
