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
  <path d="M16,30.36c-0.062,0-0.125-0.017-0.181-0.05l-12-7C3.708,23.246,3.64,23.128,3.64,23	V9c0-0.128,0.068-0.247,0.179-0.311l12-7c0.111-0.065,0.251-0.065,0.362,0l12,7c0.11,0.064,0.178,0.182,0.179,0.31	c0,0.127-0.066,0.246-0.177,0.311l-8.216,4.884C20.22,14.745,20.36,15.356,20.36,16c0,2.404-1.956,4.36-4.36,4.36	s-4.36-1.956-4.36-4.36s1.956-4.36,4.36-4.36c1.503,0,2.831,0.765,3.615,1.926l7.676-4.563L16,2.417L4.36,9.207v13.586L16,29.583	l11.64-6.79V14h0.721v9c0,0.128-0.068,0.246-0.179,0.311l-12,7C16.125,30.344,16.062,30.36,16,30.36z M16,12.36	c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64S18.007,12.36,16,12.36z"></path>
</svg>