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
  <path d="M30,29.36H20	c-0.199,0-0.36-0.161-0.36-0.36v-9c0-0.199,0.161-0.36,0.36-0.36h4.64v-3.28H7.36v3.28H12c0.199,0,0.36,0.161,0.36,0.36v9	c0,0.199-0.161,0.36-0.36,0.36H2c-0.199,0-0.36-0.161-0.36-0.36v-9c0-0.199,0.161-0.36,0.36-0.36h4.64V16	c0-0.199,0.161-0.36,0.36-0.36h8.64v-3.28H11c-0.199,0-0.36-0.161-0.36-0.36V3c0-0.199,0.161-0.36,0.36-0.36h10	c0.199,0,0.36,0.161,0.36,0.36v9c0,0.199-0.161,0.36-0.36,0.36h-4.64v3.28H25c0.199,0,0.36,0.161,0.36,0.36v3.64H30	c0.199,0,0.36,0.161,0.36,0.36v9C30.36,29.199,30.199,29.36,30,29.36z M20.36,28.64h9.279v-8.28H20.36V28.64z M2.36,28.64h9.28	v-8.28H2.36V28.64z M11.36,11.64h9.28V3.36h-9.28V11.64z M24,22.36h-2v-0.72h2V22.36z M6,22.36H4v-0.72h2V22.36z M15,5.36h-2V4.64h2	V5.36z"></path>
</svg>