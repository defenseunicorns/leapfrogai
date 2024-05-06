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
  <path d="M25,30.36H7c-0.17,0-0.316-0.119-0.352-0.285l-3-14	c-0.023-0.106,0.004-0.217,0.072-0.302C3.789,15.689,3.891,15.64,4,15.64h11.64V6h0.72v9.64H28c0.108,0,0.212,0.049,0.28,0.133	c0.068,0.085,0.095,0.196,0.071,0.302l-3,14C25.316,30.241,25.17,30.36,25,30.36z M7.291,29.64h17.418l2.846-13.28H16.36v6.329	c0.576,0.158,1,0.687,1,1.312c0,0.75-0.61,1.36-1.36,1.36s-1.36-0.61-1.36-1.36c0-0.625,0.424-1.153,1-1.312V16.36H4.445	L7.291,29.64z M16,23.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S16.353,23.36,16,23.36z M23.36,14h-0.72V5c0-0.353-0.287-0.64-0.64-0.64H10C9.647,4.36,9.36,4.647,9.36,5v9H8.64V5c0-0.75,0.61-1.36,1.36-1.36h12	c0.75,0,1.36,0.61,1.36,1.36V14z"></path>
</svg>