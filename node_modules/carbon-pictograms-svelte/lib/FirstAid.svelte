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
  <path d="M19,25.36h-6c-0.199,0-0.36-0.161-0.36-0.36v-5.64H7c-0.199,0-0.36-0.161-0.36-0.36v-6	c0-0.199,0.161-0.36,0.36-0.36h5.64V7c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v5.64H25	c0.199,0,0.36,0.161,0.36,0.36v6c0,0.199-0.161,0.36-0.36,0.36h-5.64V25C19.36,25.199,19.199,25.36,19,25.36z M13.36,24.64h5.28V19	c0-0.199,0.161-0.36,0.36-0.36h5.64v-5.28H19c-0.199,0-0.36-0.161-0.36-0.36V7.36h-5.28V13c0,0.199-0.161,0.36-0.36,0.36H7.36v5.28	H13c0.199,0,0.36,0.161,0.36,0.36V24.64z M16,31.36C7.53,31.36,0.64,24.47,0.64,16S7.53,0.64,16,0.64S31.36,7.53,31.36,16	S24.47,31.36,16,31.36z M16,1.36C7.927,1.36,1.36,7.927,1.36,16c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64	S24.072,1.36,16,1.36z"></path>
</svg>