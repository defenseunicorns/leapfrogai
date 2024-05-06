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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M16,1.36C7.927,1.36,1.36,7.927,1.36,16c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64S24.072,1.36,16,1.36z M16,26.36c-5.712,0-10.36-4.647-10.36-10.36c0-5.712,4.647-10.36,10.36-10.36S26.36,10.287,26.36,16S21.713,26.36,16,26.36z M16,6.36c-5.315,0-9.64,4.325-9.64,9.64s4.325,9.64,9.64,9.64s9.64-4.324,9.64-9.64S21.315,6.36,16,6.36z M16,21.36	c-2.956,0-5.36-2.405-5.36-5.36c0-2.956,2.404-5.36,5.36-5.36c2.955,0,5.36,2.404,5.36,5.36C21.36,18.955,18.955,21.36,16,21.36z M16,11.36c-2.559,0-4.64,2.082-4.64,4.64s2.082,4.64,4.64,4.64s4.64-2.081,4.64-4.64S18.559,11.36,16,11.36z M16,17	c0.552,0,1-0.448,1-1s-0.448-1-1-1s-1,0.448-1,1C15,16.553,15.448,17,16,17z"></path>
</svg>