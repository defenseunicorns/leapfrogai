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
  <path d="M4.36,31H3.64v-2.64H1v-0.72h2.64V25h0.72v2.64H7v0.721H4.36V31z M26,28.36H10v-0.72h16 c0.904,0,1.64-0.735,1.64-1.64V10h0.721v16C28.36,27.302,27.302,28.36,26,28.36z M4.36,22H3.64V6c0-1.301,1.059-2.36,2.36-2.36h16 v0.72H6C5.096,4.36,4.36,5.096,4.36,6V22z M28.36,7h-0.72V4.36H25V3.64h2.64V1h0.721v2.64H31v0.72h-2.64V7z"></path>
</svg>