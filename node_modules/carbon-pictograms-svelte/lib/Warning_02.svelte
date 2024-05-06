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
  <path d="M23.668,29.312l-0.359-0.623c4.522-2.61,7.331-7.473,7.331-12.688c0-8.073-6.567-14.64-14.64-14.64	C7.927,1.36,1.36,7.927,1.36,16c0,5.216,2.81,10.078,7.332,12.688l-0.36,0.623C3.587,26.573,0.64,21.473,0.64,16	C0.64,7.53,7.53,0.64,16,0.64S31.36,7.53,31.36,16C31.36,21.473,28.413,26.573,23.668,29.312z M16.36,24h-0.72V6h0.72V24z M16,28.5	c-0.552,0-1,0.448-1,1s0.448,1,1,1s1-0.448,1-1S16.552,28.5,16,28.5z"></path>
</svg>