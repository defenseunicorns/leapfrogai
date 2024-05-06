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
  <path d="M21,26.36H11C5.288,26.36,0.64,21.713,0.64,16C0.64,10.288,5.288,5.64,11,5.64h10	c5.713,0,10.36,4.647,10.36,10.36S26.713,26.36,21,26.36z M11,6.36c-5.315,0-9.64,4.325-9.64,9.64s4.325,9.64,9.64,9.64h10	c5.315,0,9.64-4.324,9.64-9.64S26.315,6.36,21,6.36h-6.64v2.28H21c4.059,0,7.36,3.302,7.36,7.36c0,4.059-3.302,7.36-7.36,7.36H11	c-4.058,0-7.36-3.302-7.36-7.36S6.942,8.64,11,8.64h0.64V6.36H11z M11,9.36c-3.661,0-6.64,2.979-6.64,6.64s2.979,6.64,6.64,6.64h10	c3.661,0,6.64-2.979,6.64-6.64S24.661,9.36,21,9.36h-6.64v2.28H21c2.404,0,4.36,1.956,4.36,4.36s-1.956,4.36-4.36,4.36H11	c-2.404,0-4.36-1.956-4.36-4.36s1.956-4.36,4.36-4.36h0.64V9.36H11z M11,12.36c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64	h10c2.007,0,3.64-1.633,3.64-3.64s-1.633-3.64-3.64-3.64C21,12.36,11,12.36,11,12.36z M12.36,11.64h1.28V9.36h-1.28V11.64z M12.36,8.64h1.28V6.36h-1.28V8.64z"></path>
</svg>