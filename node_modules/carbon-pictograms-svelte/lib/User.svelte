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
  <path d="M31.36,31h-0.72c0-6.432-4.777-12.232-11.359-13.792c-0.15-0.036-0.261-0.163-0.275-0.317	c-0.015-0.153,0.071-0.299,0.212-0.362c2.861-1.273,4.71-4.116,4.71-7.241c0-4.371-3.556-7.927-7.927-7.927	c-4.372,0-7.928,3.556-7.928,7.927c0,3.125,1.849,5.968,4.711,7.241c0.141,0.063,0.226,0.209,0.212,0.362	c-0.014,0.154-0.125,0.281-0.275,0.317C6.137,18.768,1.36,24.568,1.36,31H0.64c0-6.46,4.574-12.312,11.002-14.248	c-2.634-1.539-4.291-4.375-4.291-7.465c0-4.768,3.879-8.647,8.648-8.647c4.768,0,8.647,3.879,8.647,8.647	c0,3.09-1.656,5.926-4.29,7.465C26.786,18.688,31.36,24.54,31.36,31z"></path>
</svg>