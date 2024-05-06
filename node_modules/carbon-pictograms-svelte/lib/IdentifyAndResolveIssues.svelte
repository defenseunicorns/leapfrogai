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
  <path d="M30,1.64H2	C1.801,1.64,1.64,1.801,1.64,2v28c0,0.199,0.161,0.36,0.36,0.36h28c0.199,0,0.36-0.161,0.36-0.36V2C30.36,1.801,30.199,1.64,30,1.64	z M29.64,29.64H2.36V2.36h27.28C29.64,2.36,29.64,29.64,29.64,29.64z M8,17.36c0.244,0,0.47-0.07,0.669-0.183L14,22.509	L27.255,9.254l-0.51-0.509L14,21.491l-4.823-4.823C9.29,16.47,9.36,16.244,9.36,16c0-0.75-0.61-1.36-1.36-1.36S6.64,15.25,6.64,16	S7.25,17.36,8,17.36z M8,15.36c0.353,0,0.64,0.287,0.64,0.64S8.353,16.64,8,16.64S7.36,16.353,7.36,16S7.647,15.36,8,15.36z"></path>
</svg>