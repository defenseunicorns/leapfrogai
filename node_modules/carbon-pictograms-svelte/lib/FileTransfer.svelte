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
  <path d="M31.36,31h-0.72v-5.64H22c-0.199,0-0.36-0.161-0.36-0.36v-8.64H1.36V31H0.64V16	c0-0.199,0.161-0.36,0.36-0.36h21c0.096,0,0.188,0.038,0.255,0.105l9,9c0.067,0.067,0.105,0.159,0.105,0.255	C31.36,25,31.36,31,31.36,31z M22.36,24.64h7.771l-7.771-7.771V24.64z M31,13.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v11.64	h29.28V1h0.721v12C31.36,13.199,31.199,13.36,31,13.36z"></path>
</svg>