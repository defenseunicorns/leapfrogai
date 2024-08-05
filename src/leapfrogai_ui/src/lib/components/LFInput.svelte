<script lang="ts">
  import { Helper, Input, Textarea } from 'flowbite-svelte';
  import { twMerge } from 'tailwind-merge';
  import LFLabel from '$components/LFLabel.svelte';

  export let id: string;
  export let name: string; // for form input
  export let label: string;
  export let placeholder: string = '';
  export let autocomplete: string = 'on';
  export let value: string | number = '';
  export let maxlength: number;
  export let errorText: string | undefined = undefined;
  export let divClass: string = '';
  export let labelClass: string = '';
  export let inputClass: string = '';
  export let helperClass: string = '';
  export let tooltipText: string | undefined = undefined;
  export let hideLabel: boolean = false;
  export let textArea: boolean = false;
  export let textAreaRows: number = 6;

  let divInnerClass = twMerge('mb-6', divClass);
  let labelInnerClass = twMerge('block', labelClass);
  let helperInnerClass = twMerge('mt-2', helperClass);
</script>

<div class={divInnerClass}>
  {#if !hideLabel}
    <LFLabel {id} {labelInnerClass} {tooltipText}>{label}</LFLabel>
  {/if}
  {#if textArea}
    <Textarea
      {id}
      {name}
      {placeholder}
      {autocomplete}
      bind:value
      rows={textAreaRows}
      {maxlength}
      color={errorText ? 'red' : 'base'}
      class={inputClass}
    />
  {:else}
    <Input
      {id}
      {name}
      {placeholder}
      {autocomplete}
      bind:value
      {maxlength}
      color={errorText ? 'red' : 'base'}
      class={inputClass}
    />
  {/if}
  {#if errorText}
    <Helper class={helperInnerClass} color="red"
      ><span class="font-medium">{errorText}</span></Helper
    >
  {/if}
</div>
