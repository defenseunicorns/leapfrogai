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
  <path d="M16,0.64C7.53,0.64,0.64,7.53,0.64,16	S7.53,31.36,16,31.36S31.36,24.47,31.36,16S24.47,0.64,16,0.64z M16,30.64c-5.443,0-10.202-2.985-12.725-7.405L11,15.509	l5.746,5.746c0.141,0.141,0.368,0.141,0.509,0l9.385-9.385V14h0.721v-3.36H24v0.72h2.131L17,20.491l-5.746-5.746	c-0.141-0.141-0.368-0.141-0.509,0l-7.826,7.826C1.922,20.595,1.36,18.361,1.36,16C1.36,7.927,7.927,1.36,16,1.36	c8.072,0,14.64,6.567,14.64,14.64C30.64,24.072,24.072,30.64,16,30.64z"></path>
</svg>