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
  <path d="M17,27.36h-5v-0.72h5V27.36z M22,23.36H12v-0.72h10V23.36z M8,23.36H3v-0.72h5V23.36z M31,19.36H1v-0.72h30	V19.36z M16,16.36v-0.72c2.559,0,4.64-2.082,4.64-4.64S18.559,6.36,16,6.36S11.36,8.441,11.36,11h-0.72	c0-2.956,2.404-5.36,5.36-5.36c2.955,0,5.36,2.404,5.36,5.36S18.955,16.36,16,16.36z M28.984,15.36h-5v-0.72h5V15.36z M11,15.36H3	v-0.72h8V15.36z M8,11.36H1v-0.72h7V11.36z"></path>
</svg>