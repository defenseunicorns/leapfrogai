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
  <path d="M16,31.36c-4.058,0-7.36-3.302-7.36-7.36	c0-3.78,2.864-6.903,6.537-7.314l-6.431-6.431C8.678,10.187,8.64,10.096,8.64,10V1c0-0.199,0.161-0.36,0.36-0.36h14	c0.199,0,0.36,0.161,0.36,0.36v9c0,0.096-0.038,0.187-0.105,0.254l-6.432,6.431C20.496,17.097,23.36,20.22,23.36,24	C23.36,28.059,20.059,31.36,16,31.36z M15.999,17.36c-3.661,0-6.639,2.979-6.639,6.64s2.979,6.64,6.64,6.64s6.64-2.979,6.64-6.64	s-2.978-6.64-6.639-6.64H15.999z M12.36,12.851l3.64,3.64l3.64-3.64V1.36h-7.28C12.36,1.36,12.36,12.851,12.36,12.851z M20.36,1.36	v10.771l2.279-2.28V1.36H20.36z M9.36,9.851l2.28,2.28V1.36H9.36V9.851z M16,28.36c-2.404,0-4.36-1.956-4.36-4.36	s1.956-4.36,4.36-4.36s4.36,1.956,4.36,4.36S18.404,28.36,16,28.36z M16,20.36c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64	s3.64-1.633,3.64-3.64S18.007,20.36,16,20.36z"></path>
</svg>