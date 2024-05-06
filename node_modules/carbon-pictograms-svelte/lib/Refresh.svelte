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
  <path d="M28,31.36H4c-1.301,0-2.36-1.059-2.36-2.36V16h0.72v13c0,0.904,0.736,1.64,1.64,1.64h24 c0.904,0,1.64-0.735,1.64-1.64V9c0-0.904-0.735-1.64-1.64-1.64H7.869l5.385,5.386l-0.509,0.509L6.491,7l6.255-6.254l0.509,0.509 L7.869,6.64H28c1.302,0,2.36,1.059,2.36,2.36v20C30.36,30.302,29.302,31.36,28,31.36z"></path>
</svg>