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
  <path d="M30,30.36H8c-0.199,0-0.36-0.161-0.36-0.36	V19.36H2c-0.199,0-0.36-0.161-0.36-0.36V2c0-0.199,0.161-0.36,0.36-0.36h22c0.199,0,0.36,0.161,0.36,0.36v10.64H30	c0.199,0,0.36,0.161,0.36,0.36v17C30.36,30.199,30.199,30.36,30,30.36z M8.36,29.64h21.28V13.36h-5.28v4.329	c0.575,0.158,1,0.687,1,1.312c0,0.75-0.61,1.36-1.36,1.36s-1.36-0.61-1.36-1.36c0-0.625,0.425-1.153,1-1.312V13.36H12v-0.72h11.64	V2.36H2.36v16.28h5.28v-4.328c-0.576-0.158-1-0.686-1-1.312c0-0.75,0.61-1.36,1.36-1.36S9.36,12.25,9.36,13	c0,0.625-0.424,1.153-1,1.312v4.328H20v0.721H8.36V29.64z M24,18.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64	s0.64-0.287,0.64-0.64S24.353,18.36,24,18.36z M8,12.36c-0.353,0-0.64,0.287-0.64,0.64S7.647,13.64,8,13.64	c0.353,0,0.64-0.287,0.64-0.64S8.353,12.36,8,12.36z"></path>
</svg>