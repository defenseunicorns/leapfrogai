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
  <path d="M16.36,31h-0.72V16.36H1v-0.72h14.64v-2.026	C11.388,14.36,6.412,14.36,1,14.36v-0.72c5.432,0,10.415,0,14.64-0.774V1h0.72v11.724c6.142-1.285,10.575-4.375,12.29-11.805	l0.701,0.162c-1.823,7.902-6.514,11.102-12.991,12.397v2.162H31v0.72H16.36V31z"></path>
</svg>