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
  <path d="M7,31.36H1c-0.199,0-0.36-0.161-0.36-0.36v-6c0-0.199,0.161-0.36,0.36-0.36h6	c0.199,0,0.36,0.161,0.36,0.36v6C7.36,31.199,7.199,31.36,7,31.36z M1.36,30.64h5.28v-5.28H1.36V30.64z M31,28.36H11v-0.72h20V28.36	z M7,19.36H1c-0.199,0-0.36-0.161-0.36-0.36v-6c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v6	C7.36,19.199,7.199,19.36,7,19.36z M1.36,18.64h5.28v-5.28H1.36V18.64z M31,16.36H11v-0.72h20V16.36z M7,7.36H1	C0.801,7.36,0.64,7.199,0.64,7V1c0-0.199,0.161-0.36,0.36-0.36h6c0.199,0,0.36,0.161,0.36,0.36v6C7.36,7.199,7.199,7.36,7,7.36z M1.36,6.64h5.28V1.36H1.36V6.64z M31,4.36H11V3.64h20V4.36z"></path>
</svg>