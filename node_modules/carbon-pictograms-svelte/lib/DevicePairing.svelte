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
  <path d="M31,29.36h-9c-0.199,0-0.36-0.161-0.36-0.36v-6.64H1v-0.72h20.64v-1.28H4	c-0.75,0-1.36-0.61-1.36-1.36V4c0-0.749,0.61-1.359,1.36-1.36h22c0.75,0,1.36,0.61,1.36,1.36v8.64H31c0.199,0,0.36,0.161,0.36,0.36	v16C31.36,29.199,31.199,29.36,31,29.36z M22.36,28.64h8.279v-2.28H22.36V28.64z M22.36,25.64h8.279V13.36H22.36V25.64z M4,3.36	C3.647,3.361,3.36,3.648,3.36,4v15c0,0.353,0.287,0.64,0.64,0.64h17.64V13c0-0.199,0.161-0.36,0.36-0.36h4.64V4	c0-0.353-0.287-0.64-0.64-0.64C26,3.36,4,3.36,4,3.36z"></path>
</svg>