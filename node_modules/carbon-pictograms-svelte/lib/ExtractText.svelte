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
  <path d="M28.255,16.746l-0.51,0.509l1.386,1.385h-3.77V7	c0-0.096-0.038-0.187-0.105-0.254l-6-6C19.188,0.678,19.096,0.64,19,0.64H1C0.801,0.64,0.64,0.801,0.64,1v30	c0,0.199,0.161,0.36,0.36,0.36h24c0.199,0,0.36-0.161,0.36-0.36V19.36h3.77l-1.386,1.385l0.51,0.51L30.509,19L28.255,16.746z M19.36,1.869l4.771,4.771H19.36V1.869z M24.64,18.64H5v0.721h19.64V30.64H1.36V1.36h17.28V7c0,0.199,0.161,0.36,0.36,0.36h5.64	C24.64,7.36,24.64,18.64,24.64,18.64z M18.745,13.254l0.51-0.509L21.509,15l-2.254,2.255l-0.51-0.509l1.386-1.386L5,15.36v-0.72	h15.131L18.745,13.254z M20.131,26.64l-1.386-1.385l0.51-0.51L21.509,27l-2.254,2.255l-0.51-0.51l1.386-1.385H5v-0.72H20.131z M5,22.64h10.13l-1.385-1.385l0.509-0.51L16.509,23l-2.255,2.255l-0.509-0.51l1.385-1.385H5V22.64z"></path>
</svg>