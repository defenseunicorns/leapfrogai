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
  <path d="M24,31.36H8c-0.199,0-0.36-0.161-0.36-0.36V15.36H3c-0.199,0-0.36-0.161-0.36-0.36V5.386 c0-0.979,0.615-1.867,1.532-2.209l6.702-2.514c0.097-0.036,0.204-0.029,0.294,0.018c0.091,0.048,0.157,0.132,0.182,0.231 l0.053,0.213C11.911,3.162,13.845,4.64,16,4.64c2.154,0,4.088-1.478,4.598-3.515l0.053-0.212c0.024-0.1,0.091-0.184,0.182-0.232 c0.093-0.048,0.2-0.056,0.294-0.019l6.702,2.514c0.916,0.342,1.532,1.23,1.532,2.209V15c0,0.199-0.161,0.36-0.36,0.36h-4.64V31 C24.36,31.199,24.199,31.36,24,31.36z M8.36,30.64h15.28V8h0.721v6.64h4.279V5.386c0-0.68-0.427-1.297-1.063-1.535l-6.327-2.374 C20.594,3.738,18.416,5.36,16,5.36c-2.418,0-4.596-1.622-5.248-3.882L4.424,3.851C3.788,4.089,3.36,4.706,3.36,5.386v9.254h4.28V8 h0.72V30.64z"></path>
</svg>