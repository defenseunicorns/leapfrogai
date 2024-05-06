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
  <path d="M31,4.64H1C0.801,4.64,0.64,4.801,0.64,5v22c0,0.199,0.161,0.36,0.36,0.36h30	c0.199,0,0.36-0.161,0.36-0.36V5C31.36,4.801,31.199,4.64,31,4.64z M30.64,26.181L19.638,16.097L30.64,5.829V26.181z M15.754,19.263	c0.139,0.131,0.353,0.131,0.491,0l2.865-2.674L30.074,26.64H1.926L12.89,16.59L15.754,19.263z M30.087,5.36L16,18.508L1.913,5.36	H30.087z M12.362,16.097L1.36,26.182V5.829L12.362,16.097z"></path>
</svg>