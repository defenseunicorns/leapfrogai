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
  <path d="M22,31.36H10v-0.72h5.64v-3.286c-4.995-0.19-9-4.313-9-9.354v-4h0.72v2.64h2.28V7	c0-3.507,2.853-6.36,6.36-6.36S22.36,3.493,22.36,7v9.64h2.279V14h0.721v4c0,5.04-4.006,9.163-9,9.354v3.286H22V31.36z M7.36,17.36	V18c0,4.764,3.876,8.64,8.64,8.64s8.64-3.876,8.64-8.64v-0.64h-2.28V18c0,3.507-2.854,6.36-6.36,6.36S9.64,21.507,9.64,18v-0.64	H7.36z M16,1.36c-3.11,0-5.64,2.53-5.64,5.64v11c0,3.11,2.53,5.64,5.64,5.64s5.64-2.529,5.64-5.64V7C21.64,3.89,19.11,1.36,16,1.36z"></path>
</svg>