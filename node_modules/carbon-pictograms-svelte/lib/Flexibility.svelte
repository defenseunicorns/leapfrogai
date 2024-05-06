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
  <path d="M19.36,31h-0.72V16c0-1.301,1.059-2.36,2.36-2.36	h9.131l-2.386-2.386l0.51-0.509L31.509,14l-3.254,3.255l-0.51-0.509l2.386-2.386H21c-0.904,0-1.64,0.736-1.64,1.64V31z M16.36,31	h-0.72V1.869l-2.386,2.385l-0.509-0.509L16,0.491l3.255,3.255l-0.51,0.509L16.36,1.869V31z M13.36,31h-0.72V21	c0-0.904-0.736-1.64-1.64-1.64H1.869l2.385,2.385l-0.509,0.51L0.491,19l3.255-3.254l0.509,0.509L1.869,18.64H11	c1.301,0,2.36,1.059,2.36,2.36V31z"></path>
</svg>