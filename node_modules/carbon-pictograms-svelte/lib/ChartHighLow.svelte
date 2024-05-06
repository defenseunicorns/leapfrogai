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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v29.64H31V31.36z M24.36,26h-0.72v-2.64H21v-0.72	h2.64V7h0.721v1.64H27v0.72h-2.64V26z M16.36,26h-0.72v-6.64H13v-0.72h2.64V7h0.72v5.64H19v0.72h-2.64V26z M8.36,26H7.64v-4.64H5	v-0.72h2.64V7h0.72v3.64H11v0.72H8.36V26z"></path>
</svg>