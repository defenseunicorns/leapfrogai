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
  <path d="M26,31.36H6c-0.199,0-0.36-0.161-0.36-0.36V5.36H2V4.64h8.64V1c0-0.199,0.161-0.36,0.36-0.36h10	c0.199,0,0.36,0.161,0.36,0.36v3.64H30v0.72h-3.64V31C26.36,31.199,26.199,31.36,26,31.36z M6.36,30.64h19.28V5.36H6.36V30.64z M11.36,4.64h9.28V1.36h-9.28V4.64z M22,25.36H10v-0.72h5.64v-4.28H14c-2.404,0-4.36-1.956-4.36-4.36v-2	c0-0.199,0.161-0.36,0.36-0.36h2c1.529,0,2.877,0.792,3.656,1.986c0.19-2.23,2.066-3.986,4.344-3.986h2	c0.199,0,0.36,0.161,0.36,0.36v2c0,2.404-1.956,4.36-4.36,4.36h-1.64v6.279H22V25.36z M10.36,14.36V16c0,2.007,1.633,3.64,3.64,3.64	h1.131l-2.385-2.385l0.509-0.509l2.386,2.385V18c0-2.007-1.633-3.64-3.64-3.64H10.36z M16.869,17.64H18	c2.007,0,3.64-1.632,3.64-3.64v-1.64H20c-2.007,0-3.64,1.633-3.64,3.64v1.131l2.385-2.385l0.51,0.509L16.869,17.64z"></path>
</svg>