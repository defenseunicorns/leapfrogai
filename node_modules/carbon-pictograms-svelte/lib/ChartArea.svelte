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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v6.5l11.526-3.842	c0.138-0.045,0.292-0.003,0.387,0.107l5.83,6.801l11.758-4.899c0.111-0.047,0.238-0.034,0.338,0.033C31.3,5.767,31.36,5.879,31.36,6	v25C31.36,31.199,31.199,31.36,31,31.36z M1.36,30.64h29.28v-7.058l-7.479,3.74c-0.118,0.059-0.259,0.049-0.367-0.027l-9.787-6.851	L1.36,29.18V30.64z M1.36,22.149v6.131l11.424-8.568c0.125-0.094,0.295-0.095,0.422-0.007l9.825,6.877l7.608-3.805v-8.142	l-9.454,5.673c-0.154,0.094-0.354,0.058-0.467-0.084l-7.749-9.686L1.36,22.149z M1.36,8.259v12.872L12.746,9.746	c0.072-0.073,0.173-0.114,0.274-0.105c0.102,0.005,0.197,0.055,0.261,0.134l7.804,9.754l9.555-5.733V6.54l-11.501,4.792	c-0.145,0.059-0.311,0.021-0.412-0.098l-5.842-6.816L1.36,8.259z"></path>
</svg>