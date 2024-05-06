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
  <path d="M28.099,27.925l-4.708-8.094c-0.005-0.008-0.009-0.016-0.015-0.023l-4.016-6.905V1.36H21	c0.199,0,0.36-0.161,0.36-0.36S21.199,0.64,21,0.64H11c-0.199,0-0.36,0.161-0.36,0.36S10.801,1.36,11,1.36h1.64v11.543l-4.015,6.902	c-0.006,0.01-0.012,0.02-0.018,0.029l-4.717,8.11c-0.369,0.737-0.33,1.596,0.103,2.296c0.433,0.701,1.184,1.12,2.008,1.12h19.998	c0.823,0,1.574-0.419,2.007-1.119C28.439,29.54,28.478,28.682,28.099,27.925z M13.311,13.181c0.032-0.055,0.049-0.118,0.049-0.181	v-2.64H16V9.64h-2.64V7.36H16V6.64h-2.64V4.36H16V3.64h-2.64V1.36h5.28V13c0,0.063,0.018,0.126,0.049,0.181l3.758,6.458H9.554	L13.311,13.181z M27.394,29.862c-0.301,0.487-0.822,0.777-1.395,0.777H6.001c-0.573,0-1.094-0.29-1.396-0.777	c-0.301-0.487-0.328-1.084-0.083-1.576l4.611-7.926h13.73l4.6,7.906C27.722,28.778,27.694,29.375,27.394,29.862z"></path>
</svg>