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
  <path d="M31,31.36H19c-0.199,0-0.36-0.161-0.36-0.36v-1.639H7c-0.199,0-0.36-0.161-0.36-0.36v-5.64H1	c-0.199,0-0.36-0.161-0.36-0.36v-14c0-0.199,0.161-0.36,0.36-0.36h5.645v-5.64c0-0.199,0.161-0.36,0.36-0.36H18.64V1	c0-0.199,0.161-0.36,0.36-0.36h12c0.199,0,0.36,0.161,0.36,0.36v4c0,0.199-0.161,0.36-0.36,0.36H19c-0.199,0-0.36-0.161-0.36-0.36	V3.361H7.364v5.28H13c0.199,0,0.36,0.161,0.36,0.36v6.641h5.28v-1.641c0-0.199,0.161-0.36,0.36-0.36h12	c0.199,0,0.36,0.161,0.36,0.36v4c0,0.199-0.161,0.36-0.36,0.36H19c-0.199,0-0.36-0.161-0.36-0.36v-1.639h-5.28v6.639	c0,0.199-0.161,0.36-0.36,0.36H7.36v5.279h11.28V27c0-0.199,0.161-0.36,0.36-0.36h12c0.199,0,0.36,0.161,0.36,0.36v4	C31.36,31.199,31.199,31.36,31,31.36z M19.36,30.64h11.28v-3.28H19.36V30.64z M1.36,22.641h11.28V9.361H1.36V22.641z M19.36,17.641	h11.28v-3.279H19.36V17.641z M19.36,4.64h11.28V1.36H19.36V4.64z M11.004,19.361h-8V18.64h8V19.361z M11.004,16.36h-8v-0.72h8V16.36	z M11.004,13.361h-8v-0.72h8V13.361z"></path>
</svg>