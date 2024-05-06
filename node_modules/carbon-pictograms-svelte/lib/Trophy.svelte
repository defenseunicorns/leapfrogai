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
  <path d="M23,31.36H9v-0.72h14V31.36z M21,29.36H11v-0.72h4.64	v-6.287c-4.324-0.185-7.808-3.669-7.993-7.993H7c-2.404,0-4.36-1.956-4.36-4.36V5c0-0.199,0.161-0.36,0.36-0.36h4.64V2	c0-0.199,0.161-0.36,0.36-0.36h16c0.199,0,0.36,0.161,0.36,0.36v2.64H29c0.199,0,0.36,0.161,0.36,0.36v5	c0,2.404-1.956,4.36-4.36,4.36h-0.647c-0.185,4.324-3.669,7.808-7.993,7.993v6.287H21V29.36z M8.36,2.36V14	c0,4.213,3.427,7.64,7.64,7.64s7.64-3.427,7.64-7.64V2.36H8.36z M24.36,13.64H25c2.007,0,3.64-1.633,3.64-3.64V5.36h-4.28V13.64z M3.36,5.36V10c0,2.007,1.633,3.64,3.64,3.64h0.64V5.36H3.36z"></path>
</svg>