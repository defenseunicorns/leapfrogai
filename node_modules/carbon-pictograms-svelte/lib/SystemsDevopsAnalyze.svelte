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
  <path d="M15.819,30.311l-12-7C3.708,23.246,3.64,23.128,3.64,23V9h0.72v13.793l11.821,6.896	L15.819,30.311z M28.36,27h-0.72v-6h0.721L28.36,27L28.36,27z M23.36,27h-0.72V17h0.721L23.36,27L23.36,27z M18.36,27h-0.72v-8	h0.721L18.36,27L18.36,27z M8.36,16H7.64V6h0.72V16z M28.36,15h-0.72V9.207L16,2.417l-3.64,2.116V13h-0.72V4.325	c0-0.128,0.068-0.247,0.179-0.311l4-2.325c0.112-0.065,0.251-0.065,0.362,0l12,7C28.292,8.753,28.36,8.872,28.36,9V15z"></path>
</svg>