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
  <path d="M4.746,31.255L0.491,27l4.255-4.255l0.509,0.51L1.869,26.64H29c0.904,0,1.64-0.735,1.64-1.64v-9h0.721v9 c0,1.302-1.059,2.36-2.36,2.36H1.869l3.385,3.385L4.746,31.255z M1.36,16H0.64V7c0-1.301,1.059-2.36,2.36-2.36h27.131l-3.386-3.386 l0.51-0.509L31.509,5l-4.254,4.254l-0.51-0.509l3.386-3.386H3C2.096,5.36,1.36,6.096,1.36,7V16z"></path>
</svg>