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
  <path d="M16,30.36c-0.062,0-0.125-0.017-0.181-0.05l-12-7C3.708,23.246,3.64,23.128,3.64,23V9h0.72v13.793	L16,29.583l11.64-6.79V14h0.721v9c0,0.128-0.068,0.246-0.179,0.311l-12,7C16.125,30.344,16.062,30.36,16,30.36z M16,20.36	c-2.404,0-4.36-1.956-4.36-4.36s1.956-4.36,4.36-4.36c1.514,0,2.85,0.775,3.631,1.949l7.661-4.585L16,2.417l-3.64,2.116V10h-0.72	V4.325c0-0.128,0.068-0.247,0.179-0.311l4-2.325c0.112-0.065,0.251-0.065,0.362,0l12,7c0.109,0.064,0.178,0.182,0.179,0.309	c0,0.127-0.066,0.246-0.176,0.311l-8.205,4.911c0.244,0.544,0.381,1.146,0.381,1.78C20.36,18.404,18.404,20.36,16,20.36z M16,12.36	c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64S18.007,12.36,16,12.36z M8.36,16H7.64V6h0.72V16z"></path>
</svg>