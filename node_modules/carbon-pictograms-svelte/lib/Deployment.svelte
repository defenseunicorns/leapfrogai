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
  <path d="M30.36,30.36H22v-0.72h7.131L16.673,17.182	c-0.397,0.227-0.948,0.227-1.346,0L2.869,29.64H10v0.721H1.64V22h0.72v7.131l12.458-12.458C14.705,16.474,14.64,16.245,14.64,16	s0.065-0.474,0.178-0.673L2.36,2.869V10H1.64V1.64H10v0.72H2.869l12.458,12.458c0.397-0.227,0.948-0.227,1.346,0L29.131,2.36H22	V1.64h8.36V10h-0.72V2.869L17.182,15.327c0.113,0.199,0.179,0.428,0.179,0.673c0,0.245-0.065,0.474-0.179,0.673L29.64,29.131V22	h0.721L30.36,30.36L30.36,30.36z M16,15.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64	S16.353,15.36,16,15.36z"></path>
</svg>