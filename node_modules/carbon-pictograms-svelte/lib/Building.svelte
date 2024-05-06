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
  <path d="M31,0.64v0.72H1V0.64H31z M29.36,30.64H31v0.721H1V30.64h1.64V3h0.72v27.64h9.28V23	c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v7.64h9.279V3h0.721V30.64z M13.36,30.64h5.28v-7.28h-5.28	C13.36,23.36,13.36,30.64,13.36,30.64z M6.36,5H5.64v2h0.72C6.36,7,6.36,5,6.36,5z M5.64,13h0.72v-2H5.64V13z M5.64,19h0.72v-2H5.64	V19z M11.36,5h-0.72v2h0.72V5z M10.64,13h0.72v-2h-0.72V13z M10.64,19h0.72v-2h-0.72V19z M16.36,5h-0.72v2h0.72V5z M15.64,13h0.72	v-2h-0.72V13z M15.64,19h0.72v-2h-0.72V19z M21.36,5h-0.72v2h0.721L21.36,5L21.36,5z M20.64,13h0.721v-2H20.64V13z M20.64,19h0.721	v-2H20.64V19z M26.36,5h-0.72v2h0.721L26.36,5L26.36,5z M25.64,13h0.721v-2H25.64V13z M25.64,19h0.721v-2H25.64V19z"></path>
</svg>