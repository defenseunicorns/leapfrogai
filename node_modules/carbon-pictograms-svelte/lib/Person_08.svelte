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
  <path d="M18.36,30h-0.72v-8h0.721L18.36,30L18.36,30z M14.36,30h-0.72v-8h0.72V30z M21,20.36h-2	c-0.75,0-1.36-0.61-1.36-1.36v-9c0-0.75,0.61-1.36,1.36-1.36h2c0.75,0,1.36,0.61,1.36,1.36v9C22.36,19.75,21.75,20.36,21,20.36z M19,9.36c-0.353,0-0.64,0.287-0.64,0.64v9c0,0.353,0.287,0.64,0.64,0.64h2c0.353,0,0.64-0.287,0.64-0.64v-9	c0-0.353-0.287-0.64-0.64-0.64H19z M13,20.36h-2c-0.75,0-1.36-0.61-1.36-1.36v-9c0-0.75,0.61-1.36,1.36-1.36h2	c0.75,0,1.36,0.61,1.36,1.36v9C14.36,19.75,13.75,20.36,13,20.36z M11,9.36c-0.353,0-0.64,0.287-0.64,0.64v9	c0,0.353,0.287,0.64,0.64,0.64h2c0.353,0,0.64-0.287,0.64-0.64v-9c0-0.353-0.287-0.64-0.64-0.64H11z M16,7.36	c-1.577,0-2.86-1.283-2.86-2.86S14.423,1.64,16,1.64s2.86,1.283,2.86,2.86S17.577,7.36,16,7.36z M16,2.36	c-1.18,0-2.14,0.96-2.14,2.14S14.82,6.64,16,6.64s2.14-0.96,2.14-2.14S17.18,2.36,16,2.36z"></path>
</svg>