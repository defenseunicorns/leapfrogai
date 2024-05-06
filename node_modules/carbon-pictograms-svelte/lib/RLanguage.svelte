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
  <path d="M31,31.36H1v-0.72h30V31.36z M31.36,24V1c0-0.199-0.161-0.36-0.36-0.36H1C0.801,0.64,0.64,0.801,0.64,1	v23c0,0.199,0.161,0.36,0.36,0.36h30C31.199,24.36,31.36,24.199,31.36,24z M1.36,1.36h29.28v22.28H1.36V1.36z M13.829,12.798h2.283	L18.227,17h1.331l-2.241-4.314c1.274-0.294,1.961-1.261,1.961-2.689c0-1.778-1.022-2.773-2.731-2.773h-3.894V17h1.177v-4.202H13.829	z M13.829,11.789V8.26h2.717c0.924,0,1.471,0.504,1.471,1.4v0.729c0,0.896-0.547,1.4-1.471,1.4H13.829z"></path>
</svg>