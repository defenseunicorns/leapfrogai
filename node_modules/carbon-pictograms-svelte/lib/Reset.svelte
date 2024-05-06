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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16S7.53,0.64,16,0.64c4.529,0,8.717,1.932,11.64,5.336V1h0.721v6.36 H22V6.64h5.259C24.466,3.275,20.402,1.36,16,1.36C7.927,1.36,1.36,7.927,1.36,16c0,8.072,6.567,14.64,14.64,14.64 c8.072,0,14.64-6.567,14.64-14.64h0.721C31.36,24.47,24.47,31.36,16,31.36z"></path>
</svg>