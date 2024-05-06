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
  <path d="M31,0.64H1C0.801,0.64,0.64,0.801,0.64,1v30	c0,0.199,0.161,0.36,0.36,0.36h30c0.199,0,0.36-0.161,0.36-0.36V1C31.36,0.801,31.199,0.64,31,0.64z M30.64,30.64H6.891	c10.334-2.576,18.058-11.775,18.434-22.806l1.421,1.421l0.51-0.509L25,6.491l-2.255,2.255l0.51,0.509l1.362-1.362	C24.15,20.396,13.932,30.449,1.36,30.638V1.36h29.28C30.64,1.36,30.64,30.64,30.64,30.64z"></path>
</svg>