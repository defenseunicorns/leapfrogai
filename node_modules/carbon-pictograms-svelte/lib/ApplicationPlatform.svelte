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
  <path d="M30,31.36H2v-0.72h1.64V19.36h-3v-6.72	h6.72v6.72h-3v11.28h5.28V7.36h-3V0.64h6.72v6.72h-3v23.28h5.28V19.36h-3v-6.72h6.72v6.72h-3v11.28h5.28V7.36h-3V0.64h6.721v6.72h-3	v23.28h5.279V19.36h-3v-6.72h6.721v6.72h-3v11.28H30V31.36z M25.36,18.64h5.279v-5.28H25.36V18.64z M13.36,18.64h5.28v-5.28h-5.28	C13.36,13.36,13.36,18.64,13.36,18.64z M1.36,18.64h5.28v-5.28H1.36V18.64z M19.36,6.64h5.279V1.36H19.36V6.64z M7.36,6.64h5.28	V1.36H7.36V6.64z M28,17.36c-0.75,0-1.36-0.61-1.36-1.36s0.61-1.36,1.36-1.36s1.36,0.61,1.36,1.36S28.75,17.36,28,17.36z M28,15.36	c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S28.353,15.36,28,15.36z M4,17.36	c-0.75,0-1.36-0.61-1.36-1.36S3.25,14.64,4,14.64S5.36,15.25,5.36,16S4.75,17.36,4,17.36z M4,15.36c-0.353,0-0.64,0.287-0.64,0.64	S3.647,16.64,4,16.64S4.64,16.353,4.64,16S4.353,15.36,4,15.36z M22,5.36c-0.75,0-1.36-0.61-1.36-1.36S21.25,2.64,22,2.64	S23.36,3.25,23.36,4S22.75,5.36,22,5.36z M22,3.36c-0.353,0-0.64,0.287-0.64,0.64S21.647,4.64,22,4.64S22.64,4.353,22.64,4	S22.353,3.36,22,3.36z"></path>
</svg>