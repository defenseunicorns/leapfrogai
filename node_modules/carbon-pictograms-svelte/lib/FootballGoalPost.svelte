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
  <path d="M31,27.64H18.36V23	c0-0.199-0.161-0.36-0.36-0.36h-1.64v-3.28H24c0.199,0,0.36-0.161,0.36-0.36V1h-0.72v17.64H8.36V1H7.64v18	c0,0.199,0.161,0.36,0.36,0.36h7.64v3.279H14c-0.199,0-0.36,0.161-0.36,0.36v4.64H1v0.721h12.64V31c0,0.199,0.161,0.36,0.36,0.36h4	c0.199,0,0.36-0.161,0.36-0.36v-2.64H31V27.64z M17.64,30.64h-3.28v-7.28h3.28V30.64z"></path>
</svg>