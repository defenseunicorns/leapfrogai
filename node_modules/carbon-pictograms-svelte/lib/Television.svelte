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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V9c0-0.199,0.161-0.36,0.36-0.36h12.645L7.822,5.312	l0.357-0.625L14.94,8.55l6.805-6.805l0.51,0.509L15.869,8.64H31c0.199,0,0.36,0.161,0.36,0.36v22	C31.36,31.199,31.199,31.36,31,31.36z M1.36,30.64h29.28V9.36H1.36V30.64z M25,29.36H3c-0.199,0-0.36-0.161-0.36-0.36V11	c0-0.199,0.161-0.36,0.36-0.36h22c0.199,0,0.36,0.161,0.36,0.36v18C25.36,29.199,25.199,29.36,25,29.36z M3.36,28.64h21.28V11.36	H3.36V28.64z M28,17.36c-0.75,0-1.36-0.61-1.36-1.36s0.61-1.36,1.36-1.36s1.36,0.61,1.36,1.36S28.75,17.36,28,17.36z M28,15.36	c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S28.353,15.36,28,15.36z M28,13.36	c-0.75,0-1.36-0.61-1.36-1.36s0.61-1.36,1.36-1.36s1.36,0.61,1.36,1.36S28.75,13.36,28,13.36z M28,11.36	c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S28.353,11.36,28,11.36z"></path>
</svg>