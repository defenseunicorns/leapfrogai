<!--This component was modified from https://github.com/carbon-design-system/carbon-components-svelte/blob/master/src/TextArea/TextArea.svelte
It keeps all the Carbon Components Svelte functionality, but instead grows as multiple lines are added until it
hits the limit specified by maxRows.
It also defaults maxCount to the environment variable PUBLIC_MESSAGE_LENGTH_LIMIT
and shows an error when the user attempts to type past the maxCount limitation.
The invalid prop can still be passed to this component to validate for other conditions.
-->

<script lang="ts">
  import { WarningFilled } from 'carbon-icons-svelte';
  import type { Writable } from 'svelte/store';
  import { onMount } from 'svelte';
  import { env } from '$env/dynamic/public';

  /** Specify the textarea value */
  export let value: Writable<string>;
  /** Specify the onSubmit function */
  export let onSubmit: (e: SubmitEvent | KeyboardEvent) => Promise<void>;
  /** Specify the maxRows value */
  export let maxRows = 10;

  /** Specify the placeholder text */
  export let placeholder = '';

  /** Specify the number of cols */
  export let cols = 50;

  /** Specify the number of rows */
  export let rows = 4;

  /**
   * Specify the max character count
   */
  export let maxCount: number = Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT);

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

  /**
   * Specify an aria label for the input
   */
  export let ariaLabel: string | undefined = undefined;

  /**
   * Obtain a reference to the error state of the input text length.
   */
  export let showLengthError = false;

  $: errorId = `error-${id}`;

  let lengthInvalidText = 'Character limit reached';
  $: limitReached = $value.length === Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT);

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
  <div class:bx--text-area__wrapper={true} data-invalid={invalid || showLengthError || undefined}>
    {#if invalid || showLengthError}
      <WarningFilled class="bx--text-area__invalid-icon" />
    {/if}
    <span class="lf-text-area">
      <textarea
        bind:this={ref}
        bind:value={$value}
        aria-invalid={invalid || showLengthError || undefined}
        aria-describedby={invalid || showLengthError ? errorId : undefined}
        aria-label={ariaLabel}
        {disabled}
        {id}
        {name}
        {cols}
        {rows}
        {placeholder}
        {readonly}
        class:bx--text-area={true}
        class:bx--text-area--light={light}
        class:bx--text-area--invalid={invalid || showLengthError}
        style="--maxRows:{maxRows};"
        maxlength={maxCount + 1 ?? undefined}
        {...$$restProps}
        on:keyup={resizeTextArea}
        on:keydown={(e) => {
          resizeTextArea();
          // Allow user to type up to maxCount, but only show error once trying to add more
          // characters after hitting this limit

          // Allow Command+A / Ctrl+A for select all even when max length is reached
          if (e.key === 'a' && (e.metaKey || e.ctrlKey)) {
            return; // Do not prevent the default action for Command+A/Ctrl+A
          }
          // If limit reached and trying to delete characters
          if (limitReached && ['Backspace', 'Delete'].includes(e.key)) {
            showLengthError = false; // remove error
          }

          // Limit has previously been reached and still trying to type
          else if (
            limitReached &&
            !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight'].includes(e.key)
          ) {
            e.preventDefault(); // disallow adding character
            showLengthError = true; // throw error
          } else {
            if (e.key === 'Enter' && !e.shiftKey && ref) {
              resizeTextArea();
              onSubmit(e);
            }
          }
        }}
        on:focus
        on:blur
        on:paste
      />
    </span>
  </div>
  {#if !invalid && !showLengthError && helperText}
    <div class:bx--form__helper-text={true} class:bx--form__helper-text--disabled={disabled}>
      {helperText}
    </div>
  {/if}
  {#if invalid || showLengthError}
    <div id={errorId} class:bx--form-requirement={true}>
      {showLengthError ? lengthInvalidText : invalidText}
    </div>
  {/if}
</div>

<style lang="scss">
  .lf-text-area {
    display: flex;
    flex: 1;
    :global(.bx--text-area) {
      overflow-y: scroll;
      min-height: var(--message-input-height);
      max-height: calc(var(--maxRows) * 22px); // each row is 22px
      scrollbar-color: themes.$layer-03 themes.$layer-01;
      padding: 0.6rem 1rem; // need to slightly reduce padding to avoid having scroll bar initially
      resize: none;
    }
  }
</style>
