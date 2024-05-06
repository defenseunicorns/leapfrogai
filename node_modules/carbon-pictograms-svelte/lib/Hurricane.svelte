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
  <path d="M6,31.36v-0.72c9.684,0,15.862-3.374,17.898-9.622C22.235,23.626,19.316,25.36,16,25.36	c-5.161,0-9.36-4.199-9.36-9.36C6.64,6.238,13.696,0.64,26,0.64v0.72c-9.684,0-15.862,3.375-17.898,9.623	C9.765,8.374,12.684,6.64,16,6.64c5.161,0,9.36,4.199,9.36,9.36C25.36,25.762,18.304,31.36,6,31.36z M16,7.36	c-4.764,0-8.64,3.876-8.64,8.64s3.876,8.64,8.64,8.64s8.64-3.876,8.64-8.64S20.764,7.36,16,7.36z M16,20.36	c-2.404,0-4.36-1.956-4.36-4.36s1.956-4.36,4.36-4.36s4.36,1.956,4.36,4.36S18.404,20.36,16,20.36z M16,12.36	c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64S18.007,12.36,16,12.36z"></path>
</svg>