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
  <path d="M16.322,31.161l-0.644-0.322l4-8C19.74,22.717,19.864,22.64,20,22.64h7	c2.007,0,3.64-1.633,3.64-3.64V5c0-2.007-1.633-3.64-3.64-3.64H5C2.993,1.36,1.36,2.993,1.36,5v14c0,2.007,1.633,3.64,3.64,3.64h11	v0.721H5c-2.404,0-4.36-1.956-4.36-4.36V5c0-2.404,1.956-4.36,4.36-4.36h22c2.404,0,4.36,1.956,4.36,4.36v14	c0,2.404-1.956,4.36-4.36,4.36h-6.777L16.322,31.161z M16.36,18h-0.72v-1.64H12v-0.72h6c0.904,0,1.64-0.736,1.64-1.64	s-0.735-1.64-1.64-1.64h-4.001c-1.301,0-2.359-1.059-2.359-2.36s1.058-2.36,2.359-2.36h1.641V6h0.72v1.64H20v0.72h-6.001	c-0.904,0-1.639,0.736-1.639,1.64s0.735,1.64,1.639,1.64H18c1.302,0,2.36,1.059,2.36,2.36s-1.059,2.36-2.36,2.36h-1.64V18z"></path>
</svg>