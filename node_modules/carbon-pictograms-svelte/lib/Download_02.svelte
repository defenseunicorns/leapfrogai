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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V12c0-0.199,0.161-0.36,0.36-0.36h8v0.72H1.36v18.28h29.28V12.36H23v-0.72h8 c0.199,0,0.36,0.161,0.36,0.36v19C31.36,31.199,31.199,31.36,31,31.36z"></path><path d="M16 25.509L9.746 19.255 10.254 18.745 15.64 24.131 15.64 1 16.36 1 16.36 24.131 21.745 18.745 22.255 19.255z"></path>
</svg>