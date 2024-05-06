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
  <path d="M23,31.36H9c-0.199,0-0.36-0.161-0.36-0.36	v-3.64H1c-0.199,0-0.36-0.161-0.36-0.36V5c0-0.199,0.161-0.36,0.36-0.36h7.64V1c0-0.199,0.161-0.36,0.36-0.36h14	c0.199,0,0.36,0.161,0.36,0.36v3.64H31c0.199,0,0.36,0.161,0.36,0.36v22c0,0.199-0.161,0.36-0.36,0.36h-7.64V31	C23.36,31.199,23.199,31.36,23,31.36z M9.36,30.64h13.28V1.36H9.36V30.64z M23.36,26.64h7.279V5.36H23.36v2.28H27v0.72h-3.64v2.28	H27v0.72h-3.64v2.28H27v0.72h-3.64V26.64z M1.36,26.64h7.28V14.36H5v-0.72h3.64v-2.28H5v-0.72h3.64V8.36H5V7.64h3.64V5.36H1.36	V26.64z M20,10.36h-8V9.64h8V10.36z M20,7.36h-8V6.64h8V7.36z M20,4.36h-8V3.64h8V4.36z"></path>
</svg>