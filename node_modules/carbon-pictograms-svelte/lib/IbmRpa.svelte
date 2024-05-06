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
  <path d="M13,10c0,0.552-0.448,1-1,1s-1-0.448-1-1s0.448-1,1-1	S13,9.448,13,10z M20,9c-0.552,0-1,0.448-1,1s0.448,1,1,1s1-0.448,1-1S20.552,9,20,9z M28.36,31h-0.72V20.36H4.36V31H3.64V20	c0-0.199,0.161-0.36,0.36-0.36h8.64v-2.28H8c-0.199,0-0.36-0.161-0.36-0.36v-6.64H5V9.64h2.64V5c0-0.199,0.161-0.36,0.36-0.36h3.64	V1h0.72v3.64h7.28V1h0.721v3.64H24c0.199,0,0.36,0.161,0.36,0.36v4.64H27v0.72h-2.64V17c0,0.199-0.161,0.36-0.36,0.36h-4.64v2.279	H28c0.199,0,0.36,0.161,0.36,0.36V31z M13.36,19.64h5.28v-2.28h-5.28C13.36,17.36,13.36,19.64,13.36,19.64z M8.36,16.64h15.28V5.36	H8.36V16.64z"></path>
</svg>