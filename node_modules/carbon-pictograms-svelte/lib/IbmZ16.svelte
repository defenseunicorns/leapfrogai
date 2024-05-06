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
  <path d="M16.003,31.36H31c0.199,0,0.36-0.161,0.36-0.36V1	c0-0.199-0.161-0.36-0.36-0.36H16.003c-0.002,0-0.004,0-0.006,0H1C0.801,0.64,0.64,0.801,0.64,1v14.999c0,0.001,0,0.002,0,0.003V31	c0,0.199,0.161,0.36,0.36,0.36h14.997c0.001,0,0.002,0,0.003,0C16.001,31.36,16.002,31.36,16.003,31.36z M16.36,16.36h14.28v14.28	H16.36V16.36z M1.36,16.869L15.131,30.64H1.36V16.869z M15.64,16.36v13.771L1.869,16.36H15.64z M16.36,1.36h14.28v14.28H16.36V1.36z M15.64,1.869V15.64H1.869L15.64,1.869z M15.131,1.36L1.36,15.131V1.36H15.131z"></path>
</svg>