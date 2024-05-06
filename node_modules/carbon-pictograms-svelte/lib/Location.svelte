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
  <path d="M16,31.36c-0.086,0-0.173-0.031-0.242-0.094C15.304,30.854,4.64,21.055,4.64,12	C4.64,5.736,9.736,0.64,16,0.64S27.36,5.736,27.36,12c0,8.057-10.652,18.801-11.106,19.255C16.185,31.324,16.092,31.36,16,31.36z M16,1.36C10.133,1.36,5.36,6.133,5.36,12c0,7.98,8.992,16.933,10.629,18.495C17.601,28.819,26.64,19.103,26.64,12	C26.64,6.133,21.867,1.36,16,1.36z M16,16.36c-2.404,0-4.36-1.956-4.36-4.36S13.596,7.64,16,7.64s4.36,1.956,4.36,4.36	S18.404,16.36,16,16.36z M16,8.36c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64S18.007,8.36,16,8.36z"></path>
</svg>