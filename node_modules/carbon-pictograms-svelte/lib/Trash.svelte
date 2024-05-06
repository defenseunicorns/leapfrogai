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
  <path d="M26,31.36H6c-0.199,0-0.36-0.161-0.36-0.36V5.36H2V4.64h8.64V1c0-0.199,0.161-0.36,0.36-0.36h10 c0.199,0,0.36,0.161,0.36,0.36v3.64H30v0.72h-3.64V31C26.36,31.199,26.199,31.36,26,31.36z M6.36,30.64h19.28V5.36H6.36V30.64z M11.36,4.64h9.28V1.36h-9.28V4.64z"></path><path d="M21,27.36c-0.199,0-0.36-0.161-0.36-0.36V9c0-0.199,0.161-0.36,0.36-0.36S21.36,8.801,21.36,9v18 C21.36,27.199,21.199,27.36,21,27.36z M16,27.36c-0.199,0-0.36-0.161-0.36-0.36V9c0-0.199,0.161-0.36,0.36-0.36 S16.36,8.801,16.36,9v18C16.36,27.199,16.199,27.36,16,27.36z M11,27.36c-0.199,0-0.36-0.161-0.36-0.36V9 c0-0.199,0.161-0.36,0.36-0.36S11.36,8.801,11.36,9v18C11.36,27.199,11.199,27.36,11,27.36z"></path>
</svg>