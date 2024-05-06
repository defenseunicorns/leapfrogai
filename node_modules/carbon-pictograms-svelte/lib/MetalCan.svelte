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
  <path d="M28,7.36V6.64H14.648l11.504-5.313l-0.303-0.653	L12.932,6.64H12v0.72h0.64v4.28h-2.28V11c0-0.75-0.61-1.36-1.36-1.36S7.64,10.25,7.64,11v0.64H5v0.72h0.501l-0.842,2.526	C4.646,14.923,4.64,14.961,4.64,15v14c0,0.056,0.013,0.111,0.038,0.161l1,2C5.739,31.283,5.864,31.36,6,31.36h9h13v-0.72h-0.64V7.36	H28z M8.36,11c0-0.353,0.287-0.64,0.64-0.64S9.64,10.647,9.64,11v0.64H8.36V11z M8,12.36h2h4.741l0.899,2.699V28.64H5.36V15.36H13	v-0.72H5.499l0.76-2.28H8z M14.777,30.64H6.223l-0.64-1.279h9.835L14.777,30.64z M26.64,9.64H22v0.72h4.64v2.28H22v0.72h4.64v2.28	H22v0.72h4.64v2.28H22v0.721h4.64v2.279H22v0.721h4.64v2.279H22v0.721h4.64v2.279H22v0.721h4.64v2.279H15.583l0.739-1.479	c0.025-0.05,0.038-0.105,0.038-0.161V15c0-0.039-0.006-0.077-0.019-0.114l-0.842-2.526H16v-0.72h-2.64V7.36h13.28V9.64z"></path>
</svg>