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
  <path d="M31.36,29.36H0.64V10.64h10V7c0-2.956,2.404-5.36,5.36-5.36c2.955,0,5.36,2.404,5.36,5.36v3.64h10V29.36z M1.673,28.64h28.654L24.567,20l5.76-8.64H1.673L7.433,20L1.673,28.64z M25.433,20l5.207,7.811V12.189L25.433,20z M1.36,12.189	v15.622L6.567,20L1.36,12.189z M11.36,10.64h9.28V7c0-2.559-2.081-4.64-4.64-4.64S11.36,4.441,11.36,7V10.64z"></path>
</svg>