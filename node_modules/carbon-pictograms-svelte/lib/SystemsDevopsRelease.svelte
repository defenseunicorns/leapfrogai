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
  <path d="M23.86,25h-0.72v-8.14l-3.449,3.397l-0.506-0.514l4.315-4.249l4.314,4.249l-0.506,0.514	L23.86,16.86V25z M16.181,29.689L4.36,22.793V9H3.64v14c0,0.128,0.068,0.246,0.179,0.311l12,7L16.181,29.689z M28.36,28v-5h-0.72	v4.64h-8.28V23h-0.72v5c0,0.199,0.161,0.36,0.36,0.36h9C28.199,28.36,28.36,28.199,28.36,28z M8.36,6H7.64v10h0.72V6z M28.36,9	c0-0.128-0.068-0.247-0.179-0.311l-12-7c-0.111-0.065-0.25-0.065-0.362,0l-4,2.325c-0.111,0.064-0.179,0.183-0.179,0.311V13h0.72	V4.532L16,2.417l11.64,6.79V14h0.721L28.36,9L28.36,9z"></path>
</svg>