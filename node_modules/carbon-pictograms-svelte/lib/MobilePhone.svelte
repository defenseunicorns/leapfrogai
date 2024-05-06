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
  <path d="M25,31.36H7c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h18	c0.199,0,0.36,0.161,0.36,0.36v30C25.36,31.199,25.199,31.36,25,31.36z M7.36,30.64h17.28v-6.28H7.36V30.64z M7.36,23.64h17.28V1.36	H7.36V23.64z M17,27.5c0-0.552-0.448-1-1-1s-1,0.448-1,1s0.448,1,1,1S17,28.052,17,27.5z"></path>
</svg>