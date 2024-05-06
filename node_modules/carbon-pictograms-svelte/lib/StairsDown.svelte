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
  <path d="M31,0.64v0.72h-5.64V7c0,0.199-0.161,0.36-0.36,0.36h-5.64V13c0,0.199-0.161,0.36-0.36,0.36h-5.64V19	c0,0.199-0.161,0.36-0.36,0.36H7.36V25c0,0.199-0.161,0.36-0.36,0.36H1.36V31H0.64v-6c0-0.199,0.161-0.36,0.36-0.36h5.64V19	c0-0.199,0.161-0.36,0.36-0.36h5.64V13c0-0.199,0.161-0.36,0.36-0.36h5.64V7c0-0.199,0.161-0.36,0.36-0.36h5.64V1	c0-0.199,0.161-0.36,0.36-0.36H31z M28.745,20.745L21.36,28.13V23h-0.72v6.36H27v-0.72h-5.13l7.385-7.385L28.745,20.745z"></path>
</svg>