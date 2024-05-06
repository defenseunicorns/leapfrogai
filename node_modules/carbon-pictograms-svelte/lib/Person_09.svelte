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
  <path d="M18.36,30h-0.72V20c0-0.199,0.161-0.36,0.36-0.36h3c0.353,0,0.64-0.287,0.64-0.64v-2	c0-0.353-0.287-0.64-0.64-0.64H11c-0.353,0-0.64,0.287-0.64,0.64v2c0,0.353,0.287,0.64,0.64,0.64h3c0.199,0,0.36,0.161,0.36,0.36v10	h-0.72v-9.64H11c-0.75,0-1.36-0.61-1.36-1.36v-2c0-0.75,0.61-1.36,1.36-1.36h10c0.75,0,1.36,0.61,1.36,1.36v2	c0,0.75-0.61,1.36-1.36,1.36h-2.64V30z M16,14.36c-1.577,0-2.86-1.283-2.86-2.86S14.423,8.64,16,8.64s2.86,1.283,2.86,2.86	S17.577,14.36,16,14.36z M16,9.36c-1.18,0-2.14,0.96-2.14,2.14s0.96,2.14,2.14,2.14s2.14-0.96,2.14-2.14S17.18,9.36,16,9.36z"></path>
</svg>