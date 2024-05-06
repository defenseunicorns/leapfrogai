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
  <path d="M11,12c0,0.552-0.447,1-1,1c-0.553,0-1-0.448-1-1s0.447-1,1-1S11,11.448,11,12 M15,8c0-0.552-0.447-1-1-1	c-0.553,0-1,0.448-1,1s0.447,1,1,1S15,8.552,15,8 M21,7c0-0.552-0.447-1-1-1s-1,0.448-1,1s0.447,1,1,1S21,7.552,21,7 M10,18	c0-0.552-0.447-1-1-1c-0.553,0-1,0.448-1,1s0.447,1,1,1S10,18.552,10,18 M13,25c0-0.552-0.447-1-1-1c-0.553,0-1,0.448-1,1	s0.447,1,1,1S13,25.552,13,25 M28,10c0-0.552-0.447-1-1-1s-1,0.448-1,1s0.447,1,1,1S28,10.552,28,10 M31,31.36H1	c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v29.64H31V31.36z M4.254,28.255l-0.509-0.51l25-25l0.51,0.509L4.254,28.255z"></path>
</svg>