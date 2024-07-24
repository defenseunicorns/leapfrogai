<script>
  /**
   * @event {number} change
   * @event {number} input
   */

  import { Label } from 'flowbite-svelte';
  import { fly, fade } from 'svelte/transition';
  
  /** Specify the value of the slider */
  export let value = 0;

  /** Set the maximum slider value */
  export let max = 100;

  /** Specify the label for the max value */
  export let maxLabel = '';

  /** Set the minimum slider value */
  export let min = 0;

  /** Specify the label for the min value */
  export let minLabel = '';

  /** Set the step value */
  export let step = 1;

  /** Set the step multiplier value */
  export let stepMultiplier = 4;

  /** Set to `true` to require a value */
  export let required = false;

  /** Specify the input type */
  export let inputType = 'number';

  /** Set to `true` to disable the slider */
  export let disabled = false;

  /** Set to `true` to enable the light variant */
  export let light = false;

  /** Set to `true` to hide the text input */
  export let hideTextInput = false;

  /**
   * Set to `true` for the slider to span
   * the full width of its containing element.
   */
  export let fullWidth = false;

  /** Set an id for the slider div element */
  export let id = 'ccs-' + Math.random().toString(36);

  /** Set to `true` to indicate an invalid state */
  export let invalid = false;

  /**
   * Specify the label text.
   * Alternatively, use the "labelText" slot (e.g., `<span slot="labelText">...</span>`)
   */
  export let labelText = '';

  /** Set to `true` to visually hide the label text */
  export let hideLabel = false;

  /** Set a name for the slider element */
  export let name = '';

  /** Obtain a reference to the HTML element */
  export let ref = null;

  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let trackRef = null;
  let dragging = false;
  let holding = false;

  function startDragging() {
    dragging = true;
  }

  function startHolding() {
    holding = true;
  }

  function stopHolding() {
    holding = false;
    dragging = false;
  }

  function move() {
    if (holding) {
      startDragging();
    }
  }

  function calcValue(e) {
    if (disabled) return;

    const offsetX = e.touches ? e.touches[0].clientX : e.clientX;
    const { left, width } = trackRef.getBoundingClientRect();
    let nextValue = min + Math.round(((max - min) * ((offsetX - left) / width)) / step) * step;

    if (nextValue <= min) {
      nextValue = min;
    } else if (nextValue >= max) {
      nextValue = max;
    }

    value = nextValue;
    dispatch('input', value);
  }

  $: labelId = `label-${id}`;
  $: range = max - min;
  $: left = ((value - min) / range) * 100;
  $: {
    if (value <= min) {
      value = min;
    } else if (value >= max) {
      value = max;
    }

    if (dragging) {
      calcValue(event);
      dragging = false;
    }

    if (!holding && !disabled) {
      dispatch('change', value);
    }
  }
</script>

<svelte:window
  on:mousemove={move}
  on:touchmove={move}
  on:mouseup={stopHolding}
  on:touchend={stopHolding}
  on:touchcancel={stopHolding}
/>

<div class="range">
  <div
    class="range__wrapper"
    tabindex="0"
    on:keydown={onKeyPress}
    bind:this={element}
    role="slider"
    aria-valuemin={min}
    aria-valuemax={max}
    aria-valuenow={value}
    {id}
    on:mousedown={onTrackEvent}
    on:touchstart={onTrackEvent}
  >
    <div class="range__track" bind:this={container}>
      <div class="range__track--highlighted" bind:this={progressBar} />
      <div
        class="range__thumb"
        class:range__thumb--holding={holding}
        bind:this={thumb}
        on:touchstart={startHolding}
        on:mousedown={startDragging}
        on:mousedown={startHolding}
        on:keydown={({ shiftKey, key }) => {
          const keys = {
            ArrowDown: -1,
            ArrowLeft: -1,
            ArrowRight: 1,
            ArrowUp: 1
          };
          if (keys[key]) {
            value += step * (shiftKey ? range / step / stepMultiplier : 1) * keys[key];
          }
        }}
      >
        {#if holding || thumbHover}
          <div class="range__tooltip" in:fly={{ y: 7, duration: 200 }} out:fade={{ duration: 100 }}>
            {value}
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class:bx--form-item={true} {...$$restProps} on:click on:mouseover on:mouseenter on:mouseleave>
  <Label for={id} id={labelId}>
    <slot name="labelText">
      {labelText}
    </slot>
  </Label>

  <div class:bx--slider-container={true} style:width={fullWidth && '100%'}>
    <span class:bx--slider__range-label={true}>{minLabel || min}</span>
    <div
      bind:this={ref}
      role="presentation"
      tabindex="-1"
      class:bx--slider={true}
      class:bx--slider--disabled={disabled}
      style:max-width={fullWidth ? 'none' : undefined}
      on:mousedown={startDragging}
      on:mousedown={startHolding}
      on:touchstart={startHolding}
      on:keydown={({ shiftKey, key }) => {
        const keys = {
          ArrowDown: -1,
          ArrowLeft: -1,
          ArrowRight: 1,
          ArrowUp: 1
        };
        if (keys[key]) {
          value += step * (shiftKey ? range / step / stepMultiplier : 1) * keys[key];
        }
      }}
    >
      <div
        role="slider"
        tabindex="0"
        class:bx--slider__thumb={true}
        style:left="{left}%"
        aria-valuemax={max}
        aria-valuemin={min}
        aria-valuenow={value}
        aria-labelledby={labelId}
        {id}
      ></div>
      <div bind:this={trackRef} class:bx--slider__track={true}></div>
      <div
        class:bx--slider__filled-track={true}
        style:transform="translate(0, -50%) scaleX({left / 100})"
      ></div>
    </div>
    <span class:bx--slider__range-label={true}>{maxLabel || max}</span>
    <input
      type={hideTextInput ? 'hidden' : inputType}
      id="input-{id}"
      {name}
      class:bx--text-input={true}
      class:bx--slider-text-input={true}
      class:bx--text-input--light={light}
      class:bx--text-input--invalid={invalid}
      {value}
      aria-labelledby={$$props['aria-label'] ? undefined : labelId}
      aria-label={$$props['aria-label'] || 'Slider number input'}
      {disabled}
      {required}
      {min}
      {max}
      {step}
      on:change={({ target }) => {
        value = Number(target.value);
      }}
      data-invalid={invalid || null}
      aria-invalid={invalid || null}
    />
  </div>
</div>

<style>
  .range {
    position: relative;
    flex: 1;
  }

  .range__wrapper {
    min-width: 100%;
    position: relative;
    padding: 0.5rem;
    box-sizing: border-box;
    outline: none;
  }

  .range__wrapper:focus-visible > .range__track {
    box-shadow:
      0 0 0 2px white,
      0 0 0 3px var(--track-focus, #6185ff);
  }

  .range__track {
    height: 6px;
    background-color: var(--track-bgcolor, #d0d0d0);
    border-radius: 999px;
  }

  .range__track--highlighted {
    background-color: var(--track-highlight-bgcolor, #6185ff);
    background: var(--track-highlight-bg, linear-gradient(90deg, #6185ff, #9c65ff));
    width: 0;
    height: 6px;
    position: absolute;
    border-radius: 999px;
  }

  .range__thumb {
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    width: 20px;
    height: 20px;
    background-color: var(--thumb-bgcolor, white);
    cursor: pointer;
    border-radius: 999px;
    margin-top: -8px;
    transition: box-shadow 100ms;
    user-select: none;
    box-shadow: var(
      --thumb-boxshadow,
      0 1px 1px 0 rgba(0, 0, 0, 0.14),
      0 0px 2px 1px rgba(0, 0, 0, 0.2)
    );
  }

  .range__thumb--holding {
    box-shadow:
      0 1px 1px 0 rgba(0, 0, 0, 0.14),
      0 1px 2px 1px rgba(0, 0, 0, 0.2),
      0 0 0 6px var(--thumb-holding-outline, rgba(113, 119, 250, 0.3));
  }

  .range__tooltip {
    pointer-events: none;
    position: absolute;
    top: -33px;
    color: var(--tooltip-text, white);
    width: 38px;
    padding: 4px 0;
    border-radius: 4px;
    text-align: center;
    background-color: var(--tooltip-bgcolor, #6185ff);
    background: var(--tooltip-bg, linear-gradient(45deg, #6185ff, #9c65ff));
  }

  .range__tooltip::after {
    content: '';
    display: block;
    position: absolute;
    height: 7px;
    width: 7px;
    background-color: var(--tooltip-bgcolor, #6185ff);
    bottom: -3px;
    left: calc(50% - 3px);
    clip-path: polygon(0% 0%, 100% 100%, 0% 100%);
    transform: rotate(-45deg);
    border-radius: 0 0 0 3px;
  }
</style>
