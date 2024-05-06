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
  <path d="M24.36,30h-0.72v-5.851l-7.28-7.28V28h-0.72V16.869	l-7.28,7.28V30H7.64v-5.131l-4.386,4.386l-0.509-0.51L7.13,24.36H2v-0.72h5.851l7.28-7.28H9.126l-4.901,3.921l-0.45-0.562	l4.199-3.359H3v-0.72h4.974l-4.199-3.359l0.45-0.562l4.901,3.921h6.004L7.85,8.36H2V7.64h5.131L2.746,3.254l0.509-0.509L7.64,7.131	V2h0.72v5.851l7.28,7.28V4h0.72v11.131l7.28-7.28V2h0.721v5.131l4.385-4.385l0.51,0.509L24.869,7.64H30v0.72h-5.851l-7.28,7.28	h6.005l4.901-3.921l0.449,0.562l-4.198,3.359H29v0.72h-4.974l4.198,3.359l-0.449,0.562l-4.901-3.921h-6.005l7.28,7.28H30v0.721	h-5.131l4.386,4.385l-0.51,0.51L24.36,24.87C24.36,24.87,24.36,30,24.36,30z"></path>
</svg>