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
  <path d="M31,31.36H1v-0.72h4.64V1c0-0.133,0.073-0.255,0.19-0.317C5.948,0.621,6.089,0.627,6.2,0.701l6,4.001	c0.1,0.066,0.16,0.179,0.16,0.299v8.639h7.28V9c0-0.133,0.073-0.255,0.19-0.317c0.118-0.063,0.259-0.057,0.369,0.018l6,4	C26.3,12.767,26.36,12.879,26.36,13v17.64H31V31.36z M20.36,30.64h5.279v-4.28H24v-0.72h1.64v-9.28H22v-0.72h3.64v-2.447	l-5.279-3.52v7.967H22v0.721h-1.64V30.64z M12.36,30.64h7.28v-3.28h-7.28C12.36,27.36,12.36,30.64,12.36,30.64z M6.36,30.64h5.28	v-4.28H10v-0.72h1.64V8.36H10V7.64h1.64V5.194L6.36,1.673V9.64H10v0.72H6.36v7.28H8v0.721H6.36v9.279H10v0.721H6.36V30.64z M12.36,26.64h7.28v-2.28h-7.28C12.36,24.36,12.36,26.64,12.36,26.64z M12.36,23.64h7.28v-9.28h-7.28	C12.36,14.36,12.36,23.64,12.36,23.64z M24,28.36h-2v-0.72h2V28.36z M10,12.36H8v-0.72h2V12.36z"></path>
</svg>