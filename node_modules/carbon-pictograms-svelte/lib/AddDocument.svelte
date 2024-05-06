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
  <path d="M31,31.36H7c-0.199,0-0.36-0.161-0.36-0.36v-6.979c-3.464-1.021-6-4.23-6-8.021s2.536-7,6-8.021V1	c0-0.199,0.161-0.36,0.36-0.36h18c0.096,0,0.188,0.038,0.255,0.105l6,6C31.322,6.813,31.36,6.904,31.36,7v24	C31.36,31.199,31.199,31.36,31,31.36z M7.36,30.64h23.28V7.36H25c-0.199,0-0.36-0.161-0.36-0.36V1.36H7.36v6.441	C7.89,7.696,8.439,7.64,9,7.64c4.61,0,8.36,3.75,8.36,8.36c0,4.609-3.75,8.36-8.36,8.36c-0.561,0-1.11-0.056-1.64-0.162	C7.36,24.198,7.36,30.64,7.36,30.64z M9,8.36c-4.213,0-7.64,3.427-7.64,7.64S4.787,23.64,9,23.64s7.64-3.427,7.64-7.64	S13.213,8.36,9,8.36z M25.36,6.64h4.771L25.36,1.869V6.64z M9.36,20H8.64v-3.64H5v-0.72h3.64V12h0.72v3.64H13v0.72H9.36V20z"></path>
</svg>