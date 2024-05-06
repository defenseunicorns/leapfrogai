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
  <path d="M31,31.36H1v-0.72h30V31.36z M13.254,6.746L7,0.491L0.746,6.746l0.509,0.509L6.64,1.869V26h0.72V1.869	l5.386,5.385L13.254,6.746z M31.255,6.746L25,0.491l-6.255,6.255l0.51,0.509L24.64,1.87V26h0.721V1.87l5.385,5.385L31.255,6.746z"></path>
</svg>