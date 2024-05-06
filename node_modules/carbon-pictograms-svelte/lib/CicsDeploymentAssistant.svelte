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
  <path d="M25,29.36H4	c-0.75,0-1.36-0.61-1.36-1.36v-5h0.72v5c0,0.353,0.287,0.64,0.64,0.64h21c0.353,0,0.64-0.287,0.64-0.64v-8h0.721v8	C26.36,28.75,25.75,29.36,25,29.36z M10,17.36H6v-0.72h4c2.559,0,4.64-2.082,4.64-4.64v-2h0.72v2	C15.36,14.956,12.956,17.36,10,17.36z M26.36,16h-0.72V3.869l-3.385,3.385l-0.51-0.509L26,2.491l4.255,4.255l-0.51,0.509	L26.36,3.869V16z M9,13.36c-1.301,0-2.36-1.059-2.36-2.36S7.699,8.64,9,8.64s2.36,1.059,2.36,2.36S10.301,13.36,9,13.36z M9,9.36	c-0.904,0-1.64,0.736-1.64,1.64S8.096,12.64,9,12.64s1.64-0.736,1.64-1.64S9.904,9.36,9,9.36z M3.36,12H2.64v-2	c0-2.956,2.404-5.36,5.36-5.36h4v0.72H8c-2.559,0-4.64,2.082-4.64,4.64C3.36,10,3.36,12,3.36,12z"></path>
</svg>