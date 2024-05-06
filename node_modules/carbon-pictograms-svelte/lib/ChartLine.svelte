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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v28.377l6.314-13.529	c0.055-0.119,0.171-0.198,0.302-0.207c0.137-0.003,0.257,0.054,0.327,0.165l4.468,6.952l4.887-14.869	c0.045-0.136,0.166-0.233,0.309-0.246c0.14-0.012,0.278,0.059,0.349,0.184l6.266,11.336l6.107-10.579l0.623,0.36l-6.426,11.13	c-0.064,0.111-0.183,0.181-0.312,0.181c-0.001,0-0.002,0-0.003,0c-0.13-0.002-0.249-0.072-0.312-0.187L18.084,8.896L13.219,23.7	c-0.043,0.132-0.159,0.228-0.296,0.245c-0.136,0.021-0.272-0.045-0.348-0.163L8.05,16.744L1.565,30.64H31V31.36z"></path>
</svg>