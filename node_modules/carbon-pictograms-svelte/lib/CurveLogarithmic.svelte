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
  <path d="M16.36,31h-0.72V16.36H1v-0.72h14.64V1h0.72	v14.64h2.202c1.325-4.728,4.558-8,12.438-8v0.72c-7.321,0-10.402,2.897-11.698,7.28H31v0.72H19.107	C18.36,19.413,18.36,23.103,18.36,27h-0.72c0-3.789,0-7.499,0.737-10.64H16.36V31z"></path>
</svg>