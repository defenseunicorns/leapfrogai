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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v22.64h9.28V16c0-0.199,0.161-0.36,0.36-0.36h9.64	V8c0-0.199,0.161-0.36,0.36-0.36h10v0.72h-9.64V16c0,0.199-0.161,0.36-0.36,0.36h-9.64V24c0,0.199-0.161,0.36-0.36,0.36H1.36v6.279	H31V31.36z"></path>
</svg>