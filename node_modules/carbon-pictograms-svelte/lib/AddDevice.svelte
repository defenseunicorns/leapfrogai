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
  <path d="M31,30.36h-8c-0.199,0-0.36-0.161-0.36-0.36v-2.64H2v-0.72h20.64v-1.28H5c-0.75,0-1.36-0.61-1.36-1.36	V13.926c-1.819-1.341-3-3.499-3-5.926c0-4.058,3.302-7.36,7.36-7.36c3.938,0,7.163,3.108,7.351,7H27c0.75,0,1.36,0.61,1.36,1.36	v6.64H31c0.199,0,0.36,0.161,0.36,0.36v14C31.36,30.199,31.199,30.36,31,30.36z M23.36,29.64h7.279v-2.28H23.36V29.64z M23.36,26.64	h7.279V16.36H23.36V26.64z M4.36,14.396V24c0,0.353,0.287,0.64,0.64,0.64h17.64V16c0-0.199,0.161-0.36,0.36-0.36h4.64V9	c0-0.353-0.287-0.64-0.64-0.64H15.351c-0.188,3.892-3.414,7-7.351,7C6.677,15.36,5.434,15.009,4.36,14.396z M8,1.36	C4.339,1.36,1.36,4.339,1.36,8S4.339,14.64,8,14.64s6.64-2.979,6.64-6.64S11.661,1.36,8,1.36z M8.36,12H7.64V8.36H4V7.64h3.64V4	h0.72v3.64H12v0.72H8.36V12z"></path>
</svg>