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
  <path d="M31.36,31.36H22v-0.72h8.131l-9.386-9.385l0.51-0.51l9.385,9.386V22h0.721v9.36H31.36z M10,31.36H0.64V22 h0.72v8.131l9.386-9.386l0.509,0.51L1.869,30.64H10V31.36z M21.255,11.254l-0.51-0.509l9.386-9.386H22V0.64h9.36V10h-0.72V1.869 L21.255,11.254z M10.746,11.254L1.36,1.869V10H0.64V0.64H10v0.72H1.869l9.385,9.386L10.746,11.254z"></path>
</svg>