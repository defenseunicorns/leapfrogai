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
  <path d="M26.862,26.85C29.64,24.069,31.36,20.232,31.36,16c0-8.47-6.89-15.36-15.36-15.36S0.64,7.53,0.64,16	S7.53,31.36,16,31.36c4.232,0,8.069-1.721,10.85-4.499c0.002-0.002,0.006-0.001,0.008-0.003S26.86,26.853,26.862,26.85z M16.869,16.36h13.753c-0.092,3.763-1.607,7.174-4.032,9.72L16.869,16.36z M30.621,15.64H16.36V1.378	C24.144,1.569,30.431,7.855,30.621,15.64z M1.36,16c0-7.951,6.375-14.428,14.28-14.622V16c0,0.1,0.04,0.19,0.106,0.255L26.08,26.59	c-2.628,2.503-6.173,4.05-10.08,4.05C7.927,30.64,1.36,24.072,1.36,16z"></path>
</svg>