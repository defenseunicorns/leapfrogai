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
  <path d="M14,28.36c-2.404,0-4.36-1.956-4.36-4.36h0.72c0,2.007,1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64	s-1.632-3.64-3.64-3.64H3v-0.72h11c2.404,0,4.36,1.956,4.36,4.36S16.404,28.36,14,28.36z M27,24.36c-2.404,0-4.36-1.956-4.36-4.36	h0.721c0,2.007,1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64s-1.633-3.64-3.64-3.64H1v-0.72h26c2.404,0,4.36,1.956,4.36,4.36	S29.404,24.36,27,24.36z M21,12.36H6v-0.72h15c2.007,0,3.64-1.633,3.64-3.64S23.007,4.36,21,4.36S17.36,5.993,17.36,8h-0.72	c0-2.404,1.956-4.36,4.36-4.36S25.36,5.596,25.36,8S23.404,12.36,21,12.36z"></path>
</svg>