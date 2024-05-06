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
  <path d="M23,31.36H9c-1.301,0-2.36-1.059-2.36-2.36V3	c0-1.301,1.059-2.36,2.36-2.36h14c1.302,0,2.36,1.059,2.36,2.36v26C25.36,30.302,24.302,31.36,23,31.36z M9,1.36	C8.096,1.36,7.36,2.096,7.36,3v26c0,0.904,0.736,1.64,1.64,1.64h14c0.904,0,1.64-0.735,1.64-1.64V3c0-0.904-0.735-1.64-1.64-1.64H9z M16,28.36c-0.75,0-1.36-0.61-1.36-1.36c0-0.374,0.152-0.713,0.397-0.959l-3.35-5.862c-0.063-0.11-0.063-0.247,0-0.357l8-14	l0.625,0.357L12.415,20l3.247,5.683C15.77,25.655,15.883,25.64,16,25.64c0.75,0,1.36,0.61,1.36,1.36S16.75,28.36,16,28.36z M16,26.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S16.353,26.36,16,26.36z"></path>
</svg>