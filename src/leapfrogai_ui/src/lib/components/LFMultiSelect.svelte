<script lang="ts">
  /* This components is a modified version of the Carbon Components Svelte MultiSelect.
   It adds a button into the menu that allows uploading of files.
   It has also been converted to use Typescript.
 */

  import type {
    MultiSelectItem,
    MultiSelectItemId
  } from 'carbon-components-svelte/src/MultiSelect/MultiSelect.svelte';
  import { afterUpdate, createEventDispatcher, setContext } from 'svelte';
  import { WarningAltFilled, WarningFilled } from 'carbon-icons-svelte';
  import {
    Checkbox,
    ListBox,
    ListBoxField,
    ListBoxMenu,
    ListBoxMenuIcon,
    ListBoxMenuItem,
    ListBoxSelection
  } from 'carbon-components-svelte';

  import type { ListBoxMenuIconTranslationId } from 'carbon-components-svelte/src/ListBox/ListBoxMenuIcon.svelte';
  import type { ListBoxSelectionTranslationId } from 'carbon-components-svelte/src/ListBox/ListBoxSelection.svelte';
  import FileUploadMenuItem from '$components/FileUploadMenuItem.svelte';
  import type { FilesForm } from '$lib/types/files';

  /**
   * Set the multiselect items
   */
  export let items: ReadonlyArray<MultiSelectItem> = [];

  /**
   * Override the display of a multiselect item
   * @type {(item: MultiSelectItem) => any}
   */
  export let itemToString = (item: MultiSelectItem) => item.text || item.id;

  /**
   * Override the item name, title, labelText, or value passed to the user-selectable checkbox input as well as the hidden inputs.
   
   */
  export let itemToInput: (
    item: MultiSelectItem
  ) => { name?: string; labelText?: any; title?: string; value?: string } = (item) => {};

  /**
   * Set the selected ids
   * @type {ReadonlyArray<MultiSelectItemId>}
   */
  export let selectedIds: ReadonlyArray<MultiSelectItemId> = [];

  /** Specify the multiselect value */
  export let value = '';

  /**
   * Set the size of the combobox
   */
  export let size: 'sm' | 'lg' | 'xl' | undefined = undefined;

  /**
   * Specify the type of multiselect
   */
  export let type: 'default' | 'inline' = 'default';

  /**
   * Specify the direction of the multiselect dropdown menu
   */
  export let direction: 'bottom' | 'top' = 'bottom';

  /**
   * Specify the selection feedback after selecting items
   */
  export let selectionFeedback: 'top' | 'fixed' | 'top-after-reopen' = 'top-after-reopen';

  /** Set to `true` to disable the dropdown */
  export let disabled = false;

  /** Set to `true` to filter items */
  export let filterable = false;

  /**
   * Override the filtering logic
   * The default filtering is an exact string comparison
   */
  export let filterItem = (item: MultiSelectItem, value: string) =>
    item.text.toLowerCase().includes(value.trim().toLowerCase());

  /** Set to `true` to open the dropdown */
  export let open = false;

  /** Set to `true` to enable the light variant */
  export let light = false;

  /** Specify the locale */
  export let locale = 'en';

  /** Specify the placeholder text */
  export let placeholder = '';

  /**
   * Override the sorting logic
   * The default sorting compare the item text value
   */
  export let sortItem = (a: MultiSelectItem, b: MultiSelectItem) =>
    a.text.localeCompare(b.text, locale, { numeric: true });

  /**
   * Override the chevron icon label based on the open state.
   * Defaults to "Open menu" when closed and "Close menu" when open
   */
  export let translateWithId: ((id: ListBoxMenuIconTranslationId) => string) | undefined =
    undefined;

  /**
   * Override the label of the clear button when the input has a selection.
   * Defaults to "Clear selected item" and "Clear all items" if more than one item is selected
   */
  export let translateWithIdSelection: ((id: ListBoxSelectionTranslationId) => string) | undefined =
    undefined;

  /** Specify the title text */
  export let titleText = '';

  /** Set to `true` to pass the item to `itemToString` in the checkbox */
  export let useTitleInItem = false;

  /** Set to `true` to indicate an invalid state */
  export let invalid = false;

  /** Specify the invalid state text */
  export let invalidText = '';

  /** Set to `true` to indicate an warning state */
  export let warn = false;

  /** Specify the warning state text */
  export let warnText = '';

  /** Specify the helper text */
  export let helperText = '';

  /** Specify the list box label */
  export let label = '';

  /** Set to `true` to visually hide the label text */
  export let hideLabel = false;

  /** Set an id for the list box component */
  export let id = 'ccs-' + Math.random().toString(36);

  /**
   * Specify a name attribute for the select
   */
  export let name: string | undefined = undefined;

  /** Obtain a reference to the input HTML element */
  export let inputRef: HTMLElement | null = null;

  /** Obtain a reference to the outer div element */
  export let multiSelectRef: HTMLDivElement | null = null;

  /**
   * Obtain a reference to the field box element
   */
  export let fieldRef: HTMLDivElement | null = null;

  /**
   * Obtain a reference to the selection element
   */
  export let selectionRef: HTMLDivElement | null = null;

  /**
   * Id of the highlighted ListBoxMenuItem
   */
  export let highlightedId: null | MultiSelectItemId = null;

  /**
   * Specify the accepted file types
   */
  export let accept: ReadonlyArray<string> = [];

  /**
   * SuperValidated Form
   */
  export let filesForm: FilesForm;

  const dispatch = createEventDispatcher();

  let initialSorted = false;
  let highlightedIndex = -1;
  let prevChecked = [];

  setContext('MultiSelect', {
    declareRef: ({ key, ref }: { key: 'field' | 'selection'; ref: HTMLDivElement }) => {
      switch (key) {
        case 'field':
          fieldRef = ref;
          break;
        case 'selection':
          selectionRef = ref;
          break;
      }
    }
  });

  function change(direction: number) {
    let index = highlightedIndex + direction;
    const length = filterable ? filteredItems.length : items.length;
    if (length === 0) return;
    if (index < 0) {
      index = length - 1;
    } else if (index >= length) {
      index = 0;
    }

    let disabled = items[index].disabled;

    while (disabled) {
      index = index + direction;

      if (index < 0) {
        index = items.length - 1;
      } else if (index >= items.length) {
        index = 0;
      }

      disabled = items[index].disabled;
    }

    highlightedIndex = index;
  }

  function sort() {
    return [
      ...(checked.length > 1 ? checked.sort(sortItem) : checked),
      ...unchecked.sort(sortItem)
    ];
  }

  afterUpdate(() => {
    if (checked.length !== prevChecked.length) {
      if (selectionFeedback === 'top') {
        sortedItems = sort();
      }
      prevChecked = checked;
      selectedIds = checked.map(({ id }) => id);
      dispatch('select', {
        selectedIds,
        selected: checked,
        unselected: unchecked
      });
    }

    if (!open) {
      if (!initialSorted || selectionFeedback !== 'fixed') {
        sortedItems = sort();
        initialSorted = true;
      }

      highlightedIndex = -1;
      value = '';
    }

    items = sortedItems;
  });

  $: menuId = `menu-${id}`;
  $: inline = type === 'inline';
  $: ariaLabel = $$props['aria-label'] || 'Choose an item';
  $: sortedItems = items.map((item) => ({
    ...item,
    checked: selectedIds.includes(item.id)
  }));
  $: checked = sortedItems.filter(({ checked }) => checked);
  $: unchecked = sortedItems.filter(({ checked }) => !checked);
  $: filteredItems = sortedItems.filter((item) => filterItem(item, value));
  $: highlightedId =
    highlightedIndex > -1
      ? (filterable ? filteredItems : sortedItems)[highlightedIndex]?.id ?? null
      : null;
</script>

<svelte:window
  on:click={({ target }) => {
    if (open && multiSelectRef && !multiSelectRef.contains(target)) {
      open = false;
    }
  }}
/>

<div
  bind:this={multiSelectRef}
  class:bx--multi-select__wrapper={true}
  class:bx--list-box__wrapper={true}
  class:bx--multi-select__wrapper--inline={inline}
  class:bx--list-box__wrapper--inline={inline}
  class:bx--multi-select__wrapper--inline--invalid={inline && invalid}
>
  {#if titleText || $$slots.titleText}
    <label
      for={id}
      class:bx--label={true}
      class:bx--label--disabled={disabled}
      class:bx--visually-hidden={hideLabel}
    >
      <slot name="titleText">
        {titleText}
      </slot>
    </label>
  {/if}
  <ListBox
    role={undefined}
    {disabled}
    {invalid}
    {invalidText}
    {open}
    {light}
    {size}
    {warn}
    {warnText}
    class="bx--multi-select {direction === 'top' && 'bx--list-box--up'} {filterable &&
      'bx--combo-box'}
      {filterable && 'bx--multi-select--filterable'}
      {invalid && 'bx--multi-select--invalid'}
      {inline && 'bx--multi-select--inline'}
      {checked.length > 0 && 'bx--multi-select--selected'}"
  >
    {#if invalid}
      <WarningFilled class="bx--list-box__invalid-icon" />
    {/if}
    {#if !invalid && warn}
      <WarningAltFilled class="bx--list-box__invalid-icon bx--list-box__invalid-icon--warning" />
    {/if}
    <ListBoxField
      role="button"
      tabindex="0"
      aria-expanded={open}
      on:click={() => {
        if (disabled) return;
        if (filterable) {
          open = true;
          inputRef?.focus();
        } else {
          open = !open;
        }
      }}
      on:keydown={(e) => {
        if (filterable) {
          return;
        }
        const key = e.key;
        if ([' ', 'ArrowUp', 'ArrowDown'].includes(key)) {
          e.preventDefault();
        }
        if (key === ' ') {
          open = !open;
        } else if (key === 'Tab') {
          if (selectionRef && checked.length > 0) {
            selectionRef.focus();
          } else {
            open = false;
            fieldRef?.blur();
          }
        } else if (key === 'ArrowDown') {
          change(1);
        } else if (key === 'ArrowUp') {
          change(-1);
        } else if (key === 'Enter') {
          if (highlightedIndex > -1) {
            sortedItems = sortedItems.map((item, i) => {
              if (i !== highlightedIndex) return item;
              return { ...item, checked: !item.checked };
            });
          }
        } else if (key === 'Escape') {
          open = false;
        }
      }}
      on:focus={() => {
        if (filterable) {
          open = true;
          if (inputRef) inputRef.focus();
        }
      }}
      on:blur={(e) => {
        if (!filterable) dispatch('blur', e);
      }}
      {id}
      {disabled}
      {translateWithId}
    >
      {#if checked.length > 0}
        <ListBoxSelection
          selectionCount={checked.length}
          on:clear
          on:clear={() => {
            selectedIds = [];
            sortedItems = sortedItems.map((item) => ({
              ...item,
              checked: false
            }));
            if (fieldRef) fieldRef.blur();
          }}
          translateWithId={translateWithIdSelection}
          {disabled}
        />
      {/if}
      {#if filterable}
        <input
          bind:this={inputRef}
          bind:value
          {...$$restProps}
          role="combobox"
          tabindex="0"
          autocomplete="off"
          aria-autocomplete="list"
          aria-expanded={open}
          aria-activedescendant={highlightedId}
          aria-disabled={disabled}
          aria-controls={menuId}
          class:bx--text-input={true}
          class:bx--text-input--empty={value === ''}
          class:bx--text-input--light={light}
          on:keydown
          on:keydown|stopPropagation={({ key }) => {
            if (key === 'Enter') {
              if (highlightedId) {
                const filteredItemIndex = sortedItems.findIndex(
                  (item) => item.id === highlightedId
                );
                sortedItems = sortedItems.map((item, i) => {
                  if (i !== filteredItemIndex) return item;
                  return { ...item, checked: !item.checked };
                });
              }
            } else if (key === 'Tab') {
              open = false;
              inputRef?.blur();
            } else if (key === 'ArrowDown') {
              change(1);
            } else if (key === 'ArrowUp') {
              change(-1);
            } else if (key === 'Escape') {
              open = false;
            } else if (key === ' ') {
              if (!open) open = true;
            }
          }}
          on:keyup
          on:focus
          on:blur
          on:paste
          {disabled}
          {placeholder}
          {id}
          {name}
        />
        {#if invalid}
          <WarningFilled class="bx--list-box__invalid-icon" />
        {/if}
        {#if value}
          <ListBoxSelection
            on:clear={() => {
              value = '';
              open = false;
            }}
            translateWithId={translateWithIdSelection}
            {disabled}
            {open}
          />
        {/if}
        <ListBoxMenuIcon
          style="pointer-events: {open ? 'auto' : 'none'}"
          on:click={(e) => {
            e.stopPropagation();
            open = !open;
          }}
          {translateWithId}
          {open}
        />
      {/if}
      {#if !filterable}
        <span class:bx--list-box__label={true}>{label}</span>
        <ListBoxMenuIcon {open} {translateWithId} />
      {/if}
    </ListBoxField>
    <div style:display={open ? 'block' : 'none'}>
      <ListBoxMenu aria-label={ariaLabel} {id} aria-multiselectable="true">
        <FileUploadMenuItem
          id="file-upload"
          labelText="Upload new data source"
          {accept}
          multiple
          disableLabelChanges
          {filesForm}
          bind:open={open}
        />
        {#each filterable ? filteredItems : sortedItems as item, i (item.id)}
          <ListBoxMenuItem
            id={item.id}
            role="option"
            aria-labelledby="checkbox-{item.id}"
            aria-selected={item.checked}
            active={item.checked}
            highlighted={highlightedIndex === i}
            disabled={item.disabled}
            on:click={(e) => {
              if (item.disabled) {
                e.stopPropagation();
                return;
              }
              sortedItems = sortedItems.map((_) =>
                _.id === item.id ? { ..._, checked: !_.checked } : _
              );
              fieldRef?.focus();
            }}
            on:mouseenter={() => {
              if (item.disabled) return;
              highlightedIndex = i;
            }}
          >
            <Checkbox
              name={item.id}
              title={useTitleInItem ? itemToString(item) : undefined}
              {...itemToInput(item)}
              readonly
              tabindex="-1"
              id="checkbox-{item.id}"
              checked={item.checked}
              disabled={item.disabled}
              on:blur={() => {
                if (i === filteredItems.length - 1) open = false;
              }}
            >
              <slot slot="labelText" {item} index={i}>
                {itemToString(item)}
              </slot>
            </Checkbox>
          </ListBoxMenuItem>
        {/each}
      </ListBoxMenu>
    </div>
  </ListBox>

  {#if !inline && !invalid && !warn && helperText}
    <div class:bx--form__helper-text={true} class:bx--form__helper-text--disabled={disabled}>
      {helperText}
    </div>
  {/if}
</div>
