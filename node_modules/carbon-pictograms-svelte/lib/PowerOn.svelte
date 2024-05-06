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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16	S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M16,1.36C7.927,1.36,1.36,7.927,1.36,16	c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64S24.072,1.36,16,1.36z M16,24.36c-4.61,0-8.36-3.751-8.36-8.36	c0-3.368,2.004-6.391,5.106-7.703l0.28,0.663C10.192,10.159,8.36,12.922,8.36,16c0,4.213,3.427,7.64,7.64,7.64s7.64-3.427,7.64-7.64	c0-3.078-1.831-5.841-4.666-7.04l0.281-0.663C22.356,9.609,24.36,12.633,24.36,16C24.36,20.609,20.609,24.36,16,24.36z M16.36,16	h-0.72V5h0.72V16z"></path>
</svg>