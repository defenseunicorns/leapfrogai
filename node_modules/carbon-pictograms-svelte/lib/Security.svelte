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
  <path d="M16,31.36C9.842,31.36,4.64,26.158,4.64,20V6.786L16,0.59l11.36,6.196V20	C27.36,26.158,22.158,31.36,16,31.36z M5.36,7.214V20c0,5.768,4.873,10.64,10.64,10.64S26.64,25.768,26.64,20V7.214L16,1.41	L5.36,7.214z"></path>
</svg>