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
  <path d="M30,27.36H2c-0.75,0-1.36-0.61-1.36-1.36V4c0-0.75,0.61-1.36,1.36-1.36h8.5c0.425,0,0.833,0.203,1.088,0.543	l1.416,2.223C13.108,5.544,13.299,5.64,13.5,5.64H30c0.75,0,1.36,0.61,1.36,1.36v19C31.36,26.75,30.75,27.36,30,27.36z M2,3.36	C1.647,3.36,1.36,3.647,1.36,4v22c0,0.353,0.287,0.64,0.64,0.64h28c0.353,0,0.64-0.287,0.64-0.64V7c0-0.353-0.287-0.64-0.64-0.64	H13.5c-0.426,0-0.833-0.203-1.088-0.544l-1.416-2.223C10.892,3.456,10.7,3.36,10.5,3.36H2z"></path>
</svg>