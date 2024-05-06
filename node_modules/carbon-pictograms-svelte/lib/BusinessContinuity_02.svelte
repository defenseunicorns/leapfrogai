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
  <path d="M30,30.36H12	c-0.199,0-0.36-0.161-0.36-0.36v-8.64H11c-0.199,0-0.36-0.161-0.36-0.36v-0.64H2c-0.199,0-0.36-0.161-0.36-0.36V2	c0-0.199,0.161-0.36,0.36-0.36h18c0.199,0,0.36,0.161,0.36,0.36v8.64H21c0.199,0,0.36,0.161,0.36,0.36v0.64H30	c0.199,0,0.36,0.161,0.36,0.36v18C30.36,30.199,30.199,30.36,30,30.36z M12.36,29.64h17.28V12.36h-8.28V13	c0,0.199-0.161,0.36-0.36,0.36h-0.64V20c0,0.199-0.161,0.36-0.36,0.36h-6.64V21c0,0.199-0.161,0.36-0.36,0.36h-0.64	C12.36,21.36,12.36,29.64,12.36,29.64z M11.36,20.64h1.28v-1.28h-1.28V20.64z M13.36,19.64h6.28v-6.28H19	c-0.199,0-0.36-0.161-0.36-0.36v-0.64h-6.28v6.28H13c0.199,0,0.36,0.161,0.36,0.36V19.64z M2.36,19.64h8.28V19	c0-0.199,0.161-0.36,0.36-0.36h0.64V12c0-0.199,0.161-0.36,0.36-0.36h6.64V11c0-0.199,0.161-0.36,0.36-0.36h0.64V2.36H2.36V19.64z M19.36,12.64h1.279v-1.28H19.36V12.64z"></path>
</svg>