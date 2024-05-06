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
  <path d="M30,30.36H2c-0.199,0-0.36-0.161-0.36-0.36V2	c0-0.199,0.161-0.36,0.36-0.36h28c0.199,0,0.36,0.161,0.36,0.36v28C30.36,30.199,30.199,30.36,30,30.36z M22.36,29.64h7.279V2.36	H2.36v7.28H22c0.199,0,0.36,0.161,0.36,0.36V29.64z M12.36,29.64h9.28V10.36H2.36v9.28H12c0.199,0,0.36,0.161,0.36,0.36V29.64z M2.36,29.64h9.28v-9.28H2.36V29.64z M8,26.36H6c-0.199,0-0.36-0.161-0.36-0.36v-2c0-0.199,0.161-0.36,0.36-0.36h2	c0.199,0,0.36,0.161,0.36,0.36v2C8.36,26.199,8.199,26.36,8,26.36z M6.36,25.64h1.28v-1.28H6.36V25.64z"></path>
</svg>