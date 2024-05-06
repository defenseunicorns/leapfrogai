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
  <path d="M16,31.36c-4.53,0-8.717-1.933-11.64-5.338V31H3.64v-6.36H10v0.721H4.743 C7.535,28.725,11.598,30.64,16,30.64c8.072,0,14.64-6.567,14.64-14.64h0.721C31.36,24.47,24.47,31.36,16,31.36z M1.36,16H0.64 C0.64,7.53,7.53,0.64,16,0.64c4.53,0,8.717,1.932,11.64,5.337V1h0.721v6.36H22V6.64h5.257C24.465,3.275,20.402,1.36,16,1.36 C7.927,1.36,1.36,7.927,1.36,16z"></path>
</svg>