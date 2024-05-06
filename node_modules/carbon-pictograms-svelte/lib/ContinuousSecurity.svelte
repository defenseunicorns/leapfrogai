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
  <path d="M10.64,18c0,2.955,2.404,5.36,5.36,5.36c2.955,0,5.36-2.405,5.36-5.36v-6.723L16,8.598	l-5.36,2.68C10.64,11.278,10.64,18,10.64,18z M11.36,11.723L16,9.402l4.64,2.32V18c0,2.559-2.081,4.64-4.64,4.64	s-4.64-2.081-4.64-4.64C11.36,18,11.36,11.723,11.36,11.723z M28.36,16c0,6.815-5.545,12.36-12.36,12.36S3.64,22.815,3.64,16	c0-6.536,5.103-11.889,11.533-12.318l-1.427-1.428l0.509-0.509L16.509,4l-2.255,2.254l-0.509-0.509l1.339-1.339	C9.094,4.876,4.36,9.891,4.36,16c0,6.418,5.222,11.64,11.64,11.64S27.64,22.418,27.64,16c0-5.315-3.59-9.951-8.729-11.273	l0.18-0.697C24.548,5.434,28.36,10.356,28.36,16z"></path>
</svg>