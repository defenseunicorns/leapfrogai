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
  <path d="M16.359,31h-0.72V16.36H1v-0.72h14.64V1h0.72v14.64H31v0.72H16.359V31z M25,2	c0-0.552-0.448-1-1-1s-1,0.448-1,1s0.448,1,1,1S25,2.552,25,2z M24,31c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1	S24.552,31,24,31z M24,12c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1S24.552,12,24,12z M24,24c-0.552,0-1-0.448-1-1s0.448-1,1-1	s1,0.448,1,1S24.552,24,24,24z M28,24c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1S28.552,24,28,24z M4,24c-0.552,0-1-0.448-1-1	s0.448-1,1-1s1,0.448,1,1S4.552,24,4,24z M4,12c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1S4.552,12,4,12z M8,12	c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1S8.552,12,8,12z M8,3C7.447,3,7,2.552,7,2s0.448-1,1-1s1,0.448,1,1S8.552,3,8,3z"></path>
</svg>