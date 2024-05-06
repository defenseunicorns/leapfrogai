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
  <path d="M1.36,31H0.64v-6c0-0.199,0.161-0.36,0.36-0.36h5.64V19c0-0.199,0.161-0.36,0.36-0.36h5.64V13	c0-0.199,0.161-0.36,0.36-0.36h5.64V7c0-0.199,0.161-0.36,0.36-0.36h5.64V1c0-0.199,0.161-0.36,0.36-0.36h6v0.72h-5.64V7	c0,0.199-0.161,0.36-0.36,0.36h-5.64V13c0,0.199-0.161,0.36-0.36,0.36h-5.64V19c0,0.199-0.161,0.36-0.36,0.36H7.36V25	c0,0.199-0.161,0.36-0.36,0.36H1.36V31z M23,20.64v0.721h5.13l-7.385,7.385l0.51,0.51l7.385-7.385V27h0.721v-6.36H23z"></path>
</svg>