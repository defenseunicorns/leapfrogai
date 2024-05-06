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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v29.64H31V31.36z M14,27.36H6v-0.72h3.64v-3.28H6	c-0.199,0-0.36-0.161-0.36-0.36V11c0-0.199,0.161-0.36,0.36-0.36h3.64V7.36H6V6.64h8v0.72h-3.64v3.28H14	c0.199,0,0.36,0.161,0.36,0.36v12c0,0.199-0.161,0.36-0.36,0.36h-3.64v3.279H14V27.36z M6.36,22.64h7.28v-5.28H6.36V22.64z M6.36,16.64h7.28v-5.28H6.36V16.64z M28,23.36h-8v-0.72h3.64v-3.28H20c-0.199,0-0.36-0.161-0.36-0.36V7	c0-0.199,0.161-0.36,0.36-0.36h3.64V3.36H20V2.64h8v0.72h-3.64v3.28H28c0.199,0,0.36,0.161,0.36,0.36v12	c0,0.199-0.161,0.36-0.36,0.36h-3.64v3.279H28V23.36z M20.36,18.64h7.279v-5.28H20.36V18.64z M20.36,12.64h7.279V7.36H20.36V12.64z"></path>
</svg>