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
  <path d="M18.36,30h-0.72v-9c0-0.199,0.161-0.36,0.36-0.36h2c0.904,0,1.64-0.735,1.64-1.64v-5	c0-2.559-2.081-4.64-4.64-4.64h-2c-2.559,0-4.64,2.082-4.64,4.64v5c0,0.904,0.736,1.64,1.64,1.64h2c0.199,0,0.36,0.161,0.36,0.36v9	h-0.72v-8.64H12c-1.301,0-2.36-1.059-2.36-2.36v-5c0-2.956,2.404-5.36,5.36-5.36h2c2.955,0,5.36,2.404,5.36,5.36v5	c0,1.302-1.059,2.36-2.36,2.36h-1.64V30z M16,7.36c-1.577,0-2.86-1.283-2.86-2.86S14.423,1.64,16,1.64s2.86,1.283,2.86,2.86	S17.577,7.36,16,7.36z M16,2.36c-1.18,0-2.14,0.96-2.14,2.14S14.82,6.64,16,6.64s2.14-0.96,2.14-2.14S17.18,2.36,16,2.36z"></path>
</svg>