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
  <path d="M30,28.36H2c-0.199,0-0.36-0.161-0.36-0.36v-6	h0.72v5.64h27.28V22h0.721v6C30.36,28.199,30.199,28.36,30,28.36z M26,25.36c-0.75,0-1.36-0.61-1.36-1.36s0.61-1.36,1.36-1.36	s1.36,0.61,1.36,1.36S26.75,25.36,26,25.36z M26,23.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64	S26.353,23.36,26,23.36z M22,24.36H5v-0.72h17V24.36z M30,20.36H2c-0.199,0-0.36-0.161-0.36-0.36v-6h0.72v5.64h27.28V14h0.721v6	C30.36,20.199,30.199,20.36,30,20.36z M26,17.36c-0.75,0-1.36-0.61-1.36-1.36s0.61-1.36,1.36-1.36s1.36,0.61,1.36,1.36	S26.75,17.36,26,17.36z M26,15.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S26.353,15.36,26,15.36z M22,16.36H5v-0.72h17V16.36z M30,12.36H2c-0.199,0-0.36-0.161-0.36-0.36V4c0-0.199,0.161-0.36,0.36-0.36h28	c0.199,0,0.36,0.161,0.36,0.36v8C30.36,12.199,30.199,12.36,30,12.36z M2.36,11.64h27.28V4.36H2.36V11.64z"></path>
</svg>