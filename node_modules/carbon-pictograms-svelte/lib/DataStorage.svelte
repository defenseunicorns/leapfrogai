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
  <path d="M31,31.336H1c-0.186,0-0.336-0.15-0.336-0.336v-5h0.672v4.664h29.328V26h0.672v5	C31.336,31.186,31.186,31.336,31,31.336z M31,23.336H1c-0.186,0-0.336-0.15-0.336-0.336v-5h0.672v4.664h29.328V18h0.672v5	C31.336,23.186,31.186,23.336,31,23.336z M31,15.336H1c-0.186,0-0.336-0.15-0.336-0.336v-5h0.672v4.664h29.328V10h0.672v5	C31.336,15.186,31.186,15.336,31,15.336z M31,7.336H1c-0.186,0-0.336-0.15-0.336-0.336V2h0.672v4.664h29.328V2h0.672v5	C31.336,7.186,31.186,7.336,31,7.336z"></path>
</svg>