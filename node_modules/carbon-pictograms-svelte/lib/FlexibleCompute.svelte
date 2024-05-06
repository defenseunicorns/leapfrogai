<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M13.5,4.5C13.2,4.5,13,4.3,13,4s0.2-0.5,0.5-0.5S14,3.7,14,4S13.8,4.5,13.5,4.5z M14,11	c0-0.3-0.2-0.5-0.5-0.5S13,10.7,13,11s0.2,0.5,0.5,0.5S14,11.3,14,11z M26,30.4h-6v-0.7h2.6v-1.3H17c-0.7,0-1.4-0.6-1.4-1.4v-8	c0-0.7,0.6-1.4,1.4-1.4h12c0.7,0,1.4,0.6,1.4,1.4v8c0,0.7-0.6,1.4-1.4,1.4h-5.6v1.3H26V30.4z M16.4,26.4V27c0,0.3,0.3,0.6,0.6,0.6	h12c0.3,0,0.6-0.3,0.6-0.6v-0.6H16.4z M16.4,25.6h13.3V19c0-0.3-0.3-0.6-0.6-0.6H17c-0.3,0-0.6,0.3-0.6,0.6V25.6z M14,24.4H4	c-0.2,0-0.4-0.2-0.4-0.4v-8h0.7v7.6H14V24.4z M28.4,16h-0.7V8.4H18V7.6h10c0.2,0,0.4,0.2,0.4,0.4V16z M16,14.4H2	c-0.2,0-0.4-0.2-0.4-0.4V9c0-0.2,0.2-0.4,0.4-0.4h14c0.2,0,0.4,0.2,0.4,0.4v5C16.4,14.2,16.2,14.4,16,14.4z M2.4,13.6h13.3V9.4H2.4	V13.6z M10,11.4H4v-0.7h6V11.4z M16,7.4H2C1.8,7.4,1.6,7.2,1.6,7V2c0-0.2,0.2-0.4,0.4-0.4h14c0.2,0,0.4,0.2,0.4,0.4v5	C16.4,7.2,16.2,7.4,16,7.4z M2.4,6.6h13.3V2.4H2.4V6.6z M10,4.4H4V3.6h6V4.4z"></path>
</svg>