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
  <path d="M17.5,21.5c0,0.704-0.487,1.29-1.14,1.452V25c0,0.199-0.161,0.36-0.36,0.36s-0.36-0.161-0.36-0.36v-2.048	c-0.654-0.162-1.14-0.748-1.14-1.452c0-0.828,0.672-1.5,1.5-1.5C16.828,20,17.5,20.672,17.5,21.5z M26.355,13v18	c0,0.196-0.159,0.355-0.355,0.355H6c-0.196,0-0.355-0.159-0.355-0.355V13c0-0.196,0.159-0.355,0.355-0.355h4.64V6	c0-2.956,2.404-5.36,5.36-5.36c2.955,0,5.36,2.404,5.36,5.36v6.645H26C26.196,12.645,26.355,12.804,26.355,13z M11.359,12.645h9.28	V6c0-2.559-2.081-4.64-4.64-4.64S11.36,3.441,11.36,6L11.359,12.645z M6.355,13.355v17.289h19.289V13.355H6.355z"></path>
</svg>