<!--This component was modified from https://github.com/carbon-design-system/carbon-components-svelte/blob/master/src/TextArea/TextArea.svelte
It keeps all the Carbon Components Svelte functionality, but instead grows as multiple lines are added until it
hits the limit specified by maxRows.
It also defaults maxCount to the environment variable PUBLIC_MESSAGE_LENGTH_LIMIT
and shows an error when the text is longer than maxCount.
-->

<script lang="ts">
	import { WarningFilled } from 'carbon-icons-svelte';
	import type { Writable } from 'svelte/store';
	import { onMount } from 'svelte';

	/* Start LF modification */
	import { env } from '$env/dynamic/public';
	/* End LF modification */

	/** Specify the textarea value */
	/* Start LF modification */
	export let value: Writable<string>;
	/** Specify the onSubmit function */
	export let onSubmit: (e: SubmitEvent | KeyboardEvent) => Promise<void>;
	/** Specify the maxRows value */
	export let maxRows = 10;
	/* End LF modification */

	/** Specify the placeholder text */
	export let placeholder = '';

	/** Specify the number of cols */
	export let cols = 50;

	/** Specify the number of rows */
	export let rows = 4;

	/* Start LF modifications */
	/**
	 * Specify the max character count
	 */
	export let maxCount: number = Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT);
	/* End LF modifications */

	/** Set to `true` to enable the light variant */
	export let light = false;

	/** Set to `true` to disable the input */
	export let disabled = false;

	/** Set to `true` to use the read-only variant */
	export let readonly = false;

	/** Specify the helper text */
	export let helperText = '';

	/** Specify the label text */
	export let labelText = '';

	/** Set to `true` to visually hide the label text */
	export let hideLabel = false;

	/** Set to `true` to indicate an invalid state */
	export let invalid = false;

	/** Specify the text for the invalid state */
	export let invalidText = '';

	/** Set an id for the textarea element */
	export let id = 'ccs-' + Math.random().toString(36);

	/**
	 * Specify a name attribute for the input
	 */
	export let name: string | undefined = undefined;

	/** Obtain a reference to the textarea HTML element */
	export let ref: HTMLTextAreaElement | null = null;

	$: errorId = `error-${id}`;

	/* Start LF modifications */
	let lengthInvalid: boolean;
	let lengthInvalidText = 'Character limit reached';
	$: lengthInvalid = $value.length > maxCount;

	let inputHeight = '';
	function resizeTextArea() {
		if (ref) {
			ref.style.height = '1px';
			ref.style.height = ref.scrollHeight - 2 + 'px';
		}
	}

	onMount(() => {
		const style = getComputedStyle(document.documentElement);
		inputHeight = style.getPropertyValue('--message-input-height').trim();
		resizeTextArea();
	});

	/* End LF modifications */
</script>

<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div on:click on:mouseover on:mouseenter on:mouseleave class:bx--form-item={true}>
	{#if (labelText || $$slots.labelText) && !hideLabel}
		<div class:bx--text-area__label-wrapper={true}>
			<label
				for={id}
				class:bx--label={true}
				class:bx--visually-hidden={hideLabel}
				class:bx--label--disabled={disabled}
			>
				<slot name="labelText">
					{labelText}
				</slot>
			</label>
			{#if maxCount}
				<div class:bx--label={true} class:bx--label--disabled={disabled}>
					{$value.length}/{maxCount}
				</div>
			{/if}
		</div>
	{/if}
	<div class:bx--text-area__wrapper={true} data-invalid={invalid || lengthInvalid || undefined}>
		{#if invalid || lengthInvalid}
			<WarningFilled class="bx--text-area__invalid-icon" />
		{/if}
		<textarea
			bind:this={ref}
			bind:value={$value}
			aria-invalid={invalid || lengthInvalid || undefined}
			aria-describedby={invalid || lengthInvalid ? errorId : undefined}
			{disabled}
			{id}
			{name}
			{cols}
			{rows}
			{placeholder}
			{readonly}
			class="lf-text-area"
			class:bx--text-area={true}
			class:bx--text-area--light={light}
			class:bx--text-area--invalid={invalid || lengthInvalid}
			style="--maxRows:{maxRows};"
			maxlength={maxCount + 1 ?? undefined}
			{...$$restProps}
			on:change
			on:input={resizeTextArea}
			on:keydown={(e) => {
				// Block further input if user is past PUBLIC_MESSAGE_LENGTH_LIMIT
				// but allow deleting characters and movement in the textarea
				if (
					$value.length > Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT) &&
					!['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight'].includes(e.key)
				) {
					e.preventDefault();
				} else {
					if (e.key === 'Enter' && !e.shiftKey && ref) {
						ref.style.height = inputHeight; // reset input size if there were multiple lines
						onSubmit(e);
					}
				}
			}}
			on:keyup
			on:focus
			on:blur
			on:paste
		></textarea>
	</div>
	{#if !invalid && !lengthInvalid && helperText}
		<div class:bx--form__helper-text={true} class:bx--form__helper-text--disabled={disabled}>
			{helperText}
		</div>
	{/if}
	{#if invalid || lengthInvalid}
		<div id={errorId} class:bx--form-requirement={true}>
			{lengthInvalid ? lengthInvalidText : invalidText}
		</div>
	{/if}
</div>

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
