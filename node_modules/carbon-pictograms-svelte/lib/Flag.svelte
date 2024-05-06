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
  <path d="M4.36,31H3.64V1c0-0.199,0.161-0.36,0.36-0.36h24	c0.131,0,0.251,0.071,0.314,0.186c0.063,0.114,0.061,0.254-0.009,0.365L23.425,9l4.881,7.809c0.069,0.111,0.072,0.25,0.009,0.366	C28.251,17.289,28.131,17.36,28,17.36H4.36V31z M4.36,16.64h22.991l-4.656-7.449c-0.072-0.117-0.072-0.265,0-0.382l4.656-7.449H4.36	V16.64z"></path>
</svg>