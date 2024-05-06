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
  <path d="M15.819,30.311l-12-7C3.708,23.246,3.64,23.128,3.64,23V9h0.72v13.793l11.821,6.896	L15.819,30.311z M25,27.36c-0.149,0-0.284-0.093-0.337-0.234l-2.674-7.129l-1.655,4.144c-0.055,0.137-0.187,0.227-0.334,0.227h-3	v-0.721h2.756l1.91-4.78c0.056-0.138,0.189-0.202,0.338-0.227c0.148,0.002,0.281,0.095,0.333,0.234l2.617,6.978l1.7-5.95	c0.044-0.155,0.185-0.262,0.346-0.262h3v0.721h-2.729l-1.926,6.738c-0.042,0.149-0.176,0.255-0.331,0.261	C25.01,27.36,25.005,27.36,25,27.36z M8.36,16H7.64V6h0.72V16z M28.36,15h-0.72V9.207L16,2.417l-3.64,2.116V13h-0.72V4.325	c0-0.128,0.068-0.247,0.179-0.311l4-2.325c0.112-0.065,0.251-0.065,0.362,0l12,7C28.292,8.753,28.36,8.872,28.36,9V15z"></path>
</svg>