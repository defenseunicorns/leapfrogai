<!--
This component creates a custom version of Flowbite Svelte's Textarea component that auto grows and shrinks in height up
to a limit of maxRows. It can also show error text.
-->

<script lang="ts">
  import { twMerge } from 'tailwind-merge';
  import { getContext, onMount } from 'svelte';
  import Wrapper from 'flowbite-svelte/Wrapper.svelte';
  import { env } from '$env/dynamic/public';
  import { Helper } from 'flowbite-svelte';
  import type { Writable } from 'svelte/store';
  import UploadedFileCard from '$components/UploadedFileCard.svelte';

  const background = getContext('background');

  export let ref: HTMLInputElement | null = null;
  export let value: Writable<string>;
  export let wrappedClass: string =
    'block w-full text-sm border-0 px-0 bg-inherit dark:bg-inherit focus:outline-none focus:ring-0 disabled:cursor-not-allowed disabled:opacity-50';
  export let unWrappedClass: string =
    'p-2.5 text-sm focus:ring-primary-500 border-gray-300 focus:border-primary-500 dark:focus:ring-primary-500 dark:focus:border-primary-500 disabled:cursor-not-allowed disabled:opacity-50';
  export let innerWrappedClass: string = 'py-2 px-4 bg-white dark:bg-gray-800';
  export let headerClass: string = '';
  export let footerClass: string = '';

  export let showLengthError = false;
  export let onSubmit: (e: SubmitEvent | KeyboardEvent) => Promise<void>;
  export let invalid = false;
  export let invalidText = '';
  export let id = 'ccs-' + Math.random().toString(36);
  export let maxRows = 10;
  export let rows = '1';

  let wrapped: boolean;
  let maxLength = Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT);
  let lengthInvalidText = 'Character limit reached';
  $: wrapped = $$slots.header || $$slots.footer;
  $: errorId = `error-${id}`;

  let wrapperClass: string;
  $: wrapperClass = twMerge(
    'rounded-lg bg-gray-50',
    background ? 'dark:bg-gray-600' : 'dark:bg-gray-700',
    'text-gray-900 dark:placeholder-gray-400 dark:text-white',
    'border border-gray-200',
    background ? 'dark:border-gray-500' : 'dark:border-gray-600',
    $$props.class
  );

  let textareaClass: string;
  $: textareaClass = wrapped ? wrappedClass : twMerge(wrapperClass, unWrappedClass, 'scrollbar');

  const headerCls = (header: boolean) =>
    twMerge(
      header ? 'border-b' : 'border-t',
      'py-2 px-3 border-gray-200',
      background ? 'dark:border-gray-500' : 'dark:border-gray-600',
      header ? headerClass : footerClass
    );

  let innerWrapperClass: string;
  $: innerWrapperClass = twMerge(
    innerWrappedClass,
    $$slots.footer ? '' : 'rounded-b-lg',
    $$slots.header ? '' : 'rounded-t-lg'
  );

  $: limitReached = $value.length === maxLength;
  $: $value === '' && resizeTextArea(true);

  function resizeTextArea(reset = false) {
    if (ref) {
      ref.style.height = 'auto';

      if (reset) {
        ref.style.overflowY = 'hidden';
        return;
      }

      const scrollHeight = ref.scrollHeight + 2;
      const maxHeight = maxRows * 18; // Rows are 18px in height
      if (scrollHeight > maxHeight) {
        ref.style.height = `${maxHeight}px`;
        ref.style.overflowY = 'auto';
      } else {
        ref.style.height = `${scrollHeight}px`;
        ref.style.overflowY = 'hidden';
      }
    }
  }

  onMount(() => {
    resizeTextArea(); // prevents a pixel jump when you first type in input
  });
</script>

<Wrapper show={wrapped} class={wrapperClass}>
  {#if $$slots.header}
    <div class={headerCls(true)}>
      <slot name="header"></slot>
    </div>
  {/if}

  <Wrapper show={wrapped} class={innerWrapperClass}>
    <textarea
      {id}
      bind:this={ref}
      bind:value={$value}
      on:blur
      on:change
      on:click
      on:contextmenu
      on:focus
      on:input={() => resizeTextArea()}
      on:keyup
      on:keydown={(e) => {
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
            onSubmit(e);
          }
        }
      }}
      {rows}
      on:keypress
      on:keyup
      on:mouseenter
      on:mouseleave
      on:mouseover
      on:paste
      on:select
      {...$$restProps}
      maxlength={maxLength + 1 ?? undefined}
      class={textareaClass}
    />

    <Helper>
      <Wrapper id={errorId} show={invalid || showLengthError} class="text-red-500">
        {showLengthError ? lengthInvalidText : invalidText}
      </Wrapper>
    </Helper>
  </Wrapper>

  {#if $$slots.footer}
    <div class={headerCls(false)}>
      <slot name="footer"></slot>
    </div>
  {/if}
</Wrapper>

<!--
@component
[Go to docs](https://flowbite-svelte.com/)
## Props
@prop export let value: Writable<string>;
@prop export let wrappedClass: string = 'block text-sm border-0 px-0 bg-inherit dark:bg-inherit focus:outline-none focus:ring-0 disabled:cursor-not-allowed disabled:opacity-50';
@prop export let unWrappedClass: string = 'p-2.5 text-sm focus:ring-primary-500 border-gray-300 focus:border-primary-500 dark:focus:ring-primary-500 dark:focus:border-primary-500 disabled:cursor-not-allowed disabled:opacity-50';
@prop export let innerWrappedClass: string = 'py-2 px-4 bg-white dark:bg-gray-800';
@prop export let headerClass: string = ''
  export let footerClass: string = '';
-->

<style lang="scss">
  .scrollbar {
    scrollbar-color: #4b5563 #1f2937;
  }
</style>
