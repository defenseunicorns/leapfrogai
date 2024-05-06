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
  <path d="M16.36,31h-0.72v-5c0-5.713,4.647-10.36,10.36-10.36	h4.131l-5.386-5.386l0.51-0.509L31.509,16l-6.254,6.255l-0.51-0.51l5.386-5.385H26c-5.315,0-9.64,4.325-9.64,9.64V31z M6.746,22.255	L0.491,16l6.255-6.254l0.509,0.509L1.869,15.64H6c3.289,0,6.31,1.51,8.288,4.144l-0.576,0.432C11.872,17.766,9.061,16.36,6,16.36	H1.869l5.385,5.385L6.746,22.255z M16.36,16h-0.72V1.869l-5.386,5.385L9.746,6.746L16,0.491l6.255,6.255l-0.51,0.509L16.36,1.869V16	z"></path>
</svg>