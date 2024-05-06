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
  <path d="M30,30.36H2c-0.199,0-0.36-0.161-0.36-0.36V2c0-0.199,0.161-0.36,0.36-0.36h28	c0.199,0,0.36,0.161,0.36,0.36v28C30.36,30.199,30.199,30.36,30,30.36z M16.36,29.64h13.28V13.36H16.36V29.64z M2.36,29.64h13.28	v-7.28H2.36V29.64z M2.36,21.64h13.28V2.36H2.36V21.64z M23.36,12.64h6.279V2.36H23.36V12.64z M16.36,12.64h6.28V2.36h-6.28V12.64z"></path>
</svg>