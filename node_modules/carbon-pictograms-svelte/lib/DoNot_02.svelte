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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M5.401,5.911C2.898,8.539,1.36,12.093,1.36,16c0,8.072,6.567,14.64,14.64,14.64c3.907,0,7.462-1.538,10.09-4.041L5.401,5.911z M5.911,5.401L26.599,26.09c2.503-2.628,4.041-6.183,4.041-10.09c0-8.073-6.567-14.64-14.64-14.64	C12.093,1.36,8.539,2.898,5.911,5.401z"></path>
</svg>