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
  <path d="M20.5,31.36c-1.025,0-1.86-0.835-1.86-1.86v-0.14h-5.28v0.14c0,1.025-0.834,1.86-1.86,1.86	s-1.86-0.835-1.86-1.86v-0.14H8c-0.199,0-0.36-0.161-0.36-0.36V9c0-0.199,0.161-0.36,0.36-0.36h4.64V1c0-0.199,0.161-0.36,0.36-0.36	h6c0.199,0,0.36,0.161,0.36,0.36v7.64H24c0.199,0,0.36,0.161,0.36,0.36v20c0,0.199-0.161,0.36-0.36,0.36h-1.64v0.14	C22.36,30.525,21.525,31.36,20.5,31.36z M19.36,29.36v0.14c0,0.629,0.511,1.14,1.14,1.14s1.14-0.511,1.14-1.14v-0.14H19.36z M10.36,29.36v0.14c0,0.629,0.512,1.14,1.14,1.14s1.14-0.511,1.14-1.14v-0.14H10.36z M8.36,28.64h15.28V9.36H8.36V28.64z M13.36,8.64h5.28V1.36h-5.28C13.36,1.36,13.36,8.64,13.36,8.64z M21,25.36H11v-0.72h10V25.36z M21,22.36H11v-0.72h10V22.36z M21,19.36H11v-0.72h10V19.36z M21,16.36H11v-0.72h10V16.36z M21,13.36H11v-0.72h10V13.36z"></path>
</svg>