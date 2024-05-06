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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v29.64h2.28V25c0-0.199,0.161-0.36,0.36-0.36h6 c0.199,0,0.36,0.161,0.36,0.36v5.64h2.28V15c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v15.64h2.279V3 c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v27.64H31V31.36z M22.36,30.64h5.279V3.36H22.36V30.64z M13.36,30.64 h5.28V15.36h-5.28C13.36,15.36,13.36,30.64,13.36,30.64z M4.36,30.64h5.28v-5.28H4.36V30.64z"></path>
</svg>