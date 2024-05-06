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
  <path d="M27,31.36H5c-0.199,0-0.36-0.161-0.36-0.36v-6.64H1c-0.199,0-0.36-0.161-0.36-0.36V10	c0-0.199,0.161-0.36,0.36-0.36h3.64V1c0-0.199,0.161-0.36,0.36-0.36h22c0.199,0,0.36,0.161,0.36,0.36v8.64H31	c0.199,0,0.36,0.161,0.36,0.36v14c0,0.199-0.161,0.36-0.36,0.36h-3.64V31C27.36,31.199,27.199,31.36,27,31.36z M5.36,30.64h21.28	V18.36H5.36V30.64z M27.36,23.64h3.279V10.36H1.36v13.28h3.28V18c0-0.199,0.161-0.36,0.36-0.36h22c0.199,0,0.36,0.161,0.36,0.36	V23.64z M5.36,9.64h21.28V1.36H5.36V9.64z M27,14.36h-4v-0.72h4V14.36z"></path>
</svg>