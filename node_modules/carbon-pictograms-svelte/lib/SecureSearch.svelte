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
  <path d="M11,21.509l-4.254-4.254l0.509-0.509L11,20.491l7.745-7.746l0.51,0.509L11,21.509z M23.623,22.313	l7.202,4.001l0.35-0.629l-7.201-4.001c0.886-1.702,1.387-3.637,1.387-5.685c0-6.815-5.545-12.36-12.36-12.36S0.64,9.185,0.64,16	S6.185,28.36,13,28.36C17.511,28.36,21.464,25.932,23.623,22.313z M24.64,16c0,6.418-5.222,11.64-11.64,11.64S1.36,22.418,1.36,16	S6.582,4.36,13,4.36S24.64,9.582,24.64,16z"></path>
</svg>