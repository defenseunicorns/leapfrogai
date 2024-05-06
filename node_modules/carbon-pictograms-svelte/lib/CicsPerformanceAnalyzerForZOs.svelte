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
  <path d="M30,30.36H4	c-1.301,0-2.36-1.059-2.36-2.36V2h0.72v26c0,0.904,0.736,1.64,1.64,1.64h4.64V14h0.72v15.64h6.28V23h0.72v6.64h6.28V20h0.721v9.64	H30V30.36z M25,14.36h-4v-0.72h4c2.559,0,4.64-2.082,4.64-4.64V7h0.721v2C30.36,11.956,27.955,14.36,25,14.36z M24,10.36	c-1.302,0-2.36-1.059-2.36-2.36S22.698,5.64,24,5.64S26.36,6.699,26.36,8S25.302,10.36,24,10.36z M24,6.36	c-0.904,0-1.64,0.736-1.64,1.64S23.096,9.64,24,9.64S25.64,8.904,25.64,8S24.904,6.36,24,6.36z M18.36,9h-0.72V7	c0-2.956,2.405-5.36,5.36-5.36h4v0.72h-4c-2.559,0-4.64,2.082-4.64,4.64V9z"></path>
</svg>