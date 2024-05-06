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
  <path d="M31,31.36h-8c-0.199,0-0.36-0.161-0.36-0.36V17c0-0.199,0.161-0.36,0.36-0.36h3.64V5.36H23V4.64h4	c0.199,0,0.36,0.161,0.36,0.36v11.64H31c0.199,0,0.36,0.161,0.36,0.36v14C31.36,31.199,31.199,31.36,31,31.36z M23.36,30.64h7.279	V17.36H23.36V30.64z M5,31.36c-2.404,0-4.36-1.956-4.36-4.36S2.596,22.64,5,22.64c2.283,0,4.162,1.764,4.345,4H20v0.721H9.345	C9.162,29.597,7.283,31.36,5,31.36z M5,23.36c-2.007,0-3.64,1.633-3.64,3.64S2.993,30.64,5,30.64S8.64,29.007,8.64,27	S7.007,23.36,5,23.36z M5.36,20.5H4.64V5c0-0.199,0.161-0.36,0.36-0.36h8.64V1c0-0.133,0.073-0.255,0.19-0.317	s0.26-0.056,0.37,0.018l6,4C20.3,4.767,20.36,4.879,20.36,5s-0.06,0.233-0.161,0.299l-6,4c-0.11,0.074-0.253,0.081-0.37,0.018	C13.713,9.255,13.64,9.133,13.64,9V5.36H5.36V20.5z M14.36,1.673v6.654L19.351,5L14.36,1.673z"></path>
</svg>