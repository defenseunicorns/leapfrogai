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
  <path d="M28.36,31h-0.72v-5.237c0-5.419-3.679-10.076-8.946-11.324	c-0.15-0.036-0.261-0.163-0.275-0.316c-0.015-0.154,0.071-0.3,0.212-0.363c2.34-1.041,3.851-3.365,3.851-5.919	c0-3.573-2.907-6.48-6.48-6.48c-3.574,0-6.481,2.907-6.481,6.48c0,2.555,1.512,4.878,3.851,5.919	c0.141,0.063,0.226,0.209,0.212,0.363c-0.014,0.153-0.125,0.281-0.275,0.316c-5.27,1.248-8.949,5.905-8.949,11.324V31H3.64v-5.237	c0-5.444,3.497-10.164,8.611-11.779c-2.123-1.296-3.452-3.618-3.452-6.144c0-3.97,3.23-7.2,7.201-7.2s7.201,3.23,7.201,7.2	c0,2.525-1.329,4.847-3.452,6.144c5.114,1.615,8.611,6.334,8.611,11.779V31z M20.255,23.255l-0.51-0.51L15,27.491l-1.746-1.746	l-0.509,0.51L15,28.509L20.255,23.255z"></path>
</svg>