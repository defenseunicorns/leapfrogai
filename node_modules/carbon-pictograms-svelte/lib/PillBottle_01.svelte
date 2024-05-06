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
  <path d="M24,31.36H8c-0.199,0-0.36-0.161-0.36-0.36V7.36H6C5.801,7.36,5.64,7.199,5.64,7V1	c0-0.199,0.161-0.36,0.36-0.36h20c0.199,0,0.36,0.161,0.36,0.36v6c0,0.199-0.161,0.36-0.36,0.36h-1.64V31	C24.36,31.199,24.199,31.36,24,31.36z M8.36,30.64h15.28v-4.28H8.36V30.64z M8.36,25.64h15.28V12.36H8.36V25.64z M8.36,11.64h15.28	V7.36H8.36V11.64z M24,6.64h1.64V1.36h-1.28V5h-0.72V1.36h-3.28V5h-0.72V1.36h-3.28V5h-0.72V1.36h-3.28V5h-0.72V1.36H8.36V5H7.64	V1.36H6.36v5.28C6.36,6.64,24,6.64,24,6.64z M21,20.36H11v-0.72h10V20.36z M21,18.36H11v-0.72h10V18.36z M16,15.36h-5v-0.72h5V15.36	z"></path>
</svg>