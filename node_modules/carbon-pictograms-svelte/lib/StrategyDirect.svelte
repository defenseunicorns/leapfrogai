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
  <path d="M27,31.36H5c-0.199,0-0.36-0.161-0.36-0.36v-6c0-0.199,0.161-0.36,0.36-0.36h2.662L8.617,9.36H7	C6.801,9.36,6.64,9.199,6.64,9V1c0-0.199,0.161-0.36,0.36-0.36h4c0.199,0,0.36,0.161,0.36,0.36v1.64h2.28V1	c0-0.199,0.161-0.36,0.36-0.36h4c0.199,0,0.36,0.161,0.36,0.36v1.64h2.279V1c0-0.199,0.161-0.36,0.36-0.36h4	c0.199,0,0.36,0.161,0.36,0.36v8c0,0.199-0.161,0.36-0.36,0.36h-1.617l0.955,15.28H27c0.199,0,0.36,0.161,0.36,0.36v6	C27.36,31.199,27.199,31.36,27,31.36z M5.36,30.64h21.28v-5.28H5.36V30.64z M8.383,24.64h15.234l-0.267-4.28H21v-0.72h2.305	L23.1,16.36H16v-0.72h7.055l-0.205-3.28H19v-0.72h3.805l-0.143-2.28H9.338L8.571,21.64H12v0.721H8.526L8.383,24.64z M7.36,8.64	h17.28V1.36h-3.28V3c0,0.199-0.161,0.36-0.36,0.36h-3c-0.199,0-0.36-0.161-0.36-0.36V1.36h-3.28V3c0,0.199-0.161,0.36-0.36,0.36h-3	c-0.199,0-0.36-0.161-0.36-0.36V1.36H7.36V8.64z"></path>
</svg>