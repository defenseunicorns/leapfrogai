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
  <path d="M7,12.36c-0.013,0-0.026,0-0.04-0.002c-0.198-0.022-0.34-0.2-0.318-0.397C7.167,7.217,11.189,3.64,16,3.64	s8.834,3.577,9.357,8.32c0.022,0.198-0.12,0.375-0.318,0.397c-0.19,0.023-0.376-0.121-0.396-0.318C24.158,7.662,20.443,4.36,16,4.36	s-8.158,3.302-8.642,7.68C7.337,12.224,7.182,12.36,7,12.36z M24.623,16l-3.662,11.903L16.348,16h-0.695L11.04,27.903L7.377,16	H6.624l4,13h0.763L16,17.095L20.614,29h0.763l4-13H24.623z"></path>
</svg>